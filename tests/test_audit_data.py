from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.models.magic.auditLog import AuditLog as AuditLogModel
from core.migration_from_magic.auditLog import AuditLog
from core.migration_from_magic.serverAudit import ServerAudit
from core.migration_from_magic.serverAuditMulti import ServerAuditMulti
from core.migration_from_magic.hddModels import HddModels
from core.components.part_specification import PartSpecification \
    as PartSpecificationComponent
from core.migration_from_magic.cleaning import Cleaning
from core.models.object import Object as ObjectModel
from core.components.data import Data as DataComponent

import pprint
from core import db
import unittest
from operator import itemgetter
import simplejson
import re


app = Flask(__name__)

app.config.from_pyfile("core/app.cfg")
db = SQLAlchemy(app)
db.init_app(app)

class AuditDataTest(unittest.TestCase):
    def migrate(self, server_id):
        migrate1 = AuditLog()
        migrate1.run_one(server_id, True)
    
        migrate2 = ServerAudit()
        migrate2.run_one(server_id, True)
    
        migrate3 = ServerAuditMulti()
        migrate3.run_one(server_id, True)
        
    def get_details(self, server_id):
        details = PartSpecificationComponent.get_by_object_name_and_type('server', server_id)
    
        return details
    
    def insert_from_audit_log(self, server_id):
        audit_log = AuditLogModel()
        response = audit_log.get_by_server(server_id)
        if response:
            data = response[0]

            params = {
                'lspci': data.lspci,
                'server_id': server_id, 
                'lsi_level': self.process_lsi_level(data.lsi_level),
                'lsiutil_level': self.process_lsiutil_level(data.lsiutil_level),
                'lsi': data.lsi,
                'cpu': data.cpu,
                'dmi': data.dmi,
                'scsi': data.scsi,
                'dmesg': data.dmesg,
                'fdisk': data.fdisk,
                'dmraid': self.process_dmraid(data.dmraid),
                'sas2_level': data.sas2_level,
                'usb': data.usb
            }
            
            if params['lspci'] is None and params['lsi_level'] is None and params['cpu'] is None:
                return False

            object_model = ObjectModel()
            object_id = object_model.assure(params['server_id'], 'server')
            
            try: 
                DataComponent.update(object_id, params)
                psc = PartSpecificationComponent(object_id)
                psc.update()
            except Exception as e:
                print('!!!!!!!!!!!!!!    Exception    !!!!!!!!!!!!!!!!')
                print(str(e))
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                
        return True
        
    def prepare(self, details):
        new_details = {}
        for key in details.keys():
            values = list(details[key].values())
            new_values = []
            for value in values:
                new_list = sorted(value['specification'], key=itemgetter('option'))
                new_values.append(new_list)
                
            new_details[key] = new_values
            
        if 'raid' in new_details:
            index = 0
            for part in new_details['raid']:
                if part[0]['option'] == 'productName':
                    del new_details['raid'][index]
                    new_details['raid'].insert(0, part)
                    
                index = index + 1
                
                    
            
        return new_details
    
    def process_lsiutil_level(self, output):
        if output:
            output = output.strip(' \t\n\r')
            match = re.search(
                r'0 MPT Ports found',
                output
            )
        
            if match:
                output = ''
    
        return output

    def process_lsi_level(self, output):
        if output:
            output = output.strip(' \t\n\r')
            if output == 'Exit Code: 0x00':
                output = ''
    
        return output
    
    def process_dmraid(self, output):
        if output:
            output = output.strip(' \t\n\r')
            if output == 'no raid disks':
                output = ''
    
        return output
    
    
    def test(self):
        Cleaning.truncate_all()
        
        migrate0 = HddModels()
        migrate0.run_real()
        
        limit = 100
        audit_log = AuditLogModel()
        for i in range(10):
            offset = i * limit;
            server_ids = audit_log.get_server_ids(limit, offset)

            migrated = {}
            processed = {}
            
            for server_id in server_ids:
                if not server_id:
                    continue
                
                print('================> ' + str(server_id))
                pp = pprint.PrettyPrinter(indent=4)
                
                self.migrate(server_id)
                
                details1 = self.get_details(server_id)
                details1 = self.prepare(details1)
                
    
                result = self.insert_from_audit_log(server_id)
                
                if result:
                    details2 = self.get_details(server_id)
                    details2 = self.prepare(details2)
                    
                    migrated[server_id] = details1
                    processed[server_id] = details2
                
                #self.maxDiff = None
                #self.assertEqual(details1, details2)
    
            migrated_file = open("diff/migrated"+str(i)+".txt", "w")
            migrated_file.write(simplejson.dumps(migrated, indent=4, sort_keys=True))
            migrated_file.close()
            
            processed_file = open("diff/processed"+str(i)+".txt", "w")
            processed_file.write(simplejson.dumps(processed, indent=4, sort_keys=True))
            processed_file.close()
    




