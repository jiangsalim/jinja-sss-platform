import random, string
from datetime import datetime

class IDGenerator:
    PREFIXES = {'student':'JSSS','teacher':'TCH','head_teacher':'HDT','deputy_academics':'DHA','deputy_welfare':'DHW','registrar':'ACR','director_studies':'DOS','finance':'FIN','hr':'HR','hod':'HOD','head_admin':'HOA','head_discipline':'HDS','nurse':'NUR','counselor':'CNS','chaplain':'CHP','social_worker':'SWK','lab_technician':'LAB','receptionist':'REC','records_clerk':'RCD','procurement':'PRO','store_keeper':'STO','security_head':'SEC','security_guard':'SG','maintenance':'MNT','groundskeeper':'GRD','cleaner':'CLN','chef':'KCH','kitchen_staff':'KST','transport_manager':'TRM','bus_driver':'DRV','ict_manager':'ICT','ict_technician':'ICT','librarian':'LIB','library_assistant':'LBA','prefect_coordinator':'PRF'}
    @staticmethod
    def generate_entity_id(prefix, last=0): return f"{prefix}-{last+1:03d}"
    @staticmethod
    def generate_receipt_number():
        d = datetime.now().strftime('%Y%m%d')
        r = ''.join(random.choices(string.digits, k=3))
        return f"RCP-{d}-{r}"
    @staticmethod
    def generate_transaction_id():
        d = datetime.now().strftime('%Y%m%d')
        r = ''.join(random.choices(string.ascii_uppercase+string.digits, k=6))
        return f"TXN-{d}-{r}"
    @staticmethod
    def generate_reset_token(): return ''.join(random.choices(string.ascii_letters+string.digits, k=64))
    @staticmethod
    def generate_file_name(orig):
        ext = orig.split('.')[-1] if '.' in orig else ''
        ts = datetime.now().strftime('%Y%m%d%H%M%S')
        r = ''.join(random.choices(string.ascii_lowercase+string.digits, k=8))
        return f"{ts}_{r}.{ext}" if ext else f"{ts}_{r}"
