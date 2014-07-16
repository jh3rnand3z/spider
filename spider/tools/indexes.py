
def ensure_indexes(db):
    '''
        Ensure database indexes
    '''
    db.outbound.ensure_index([('uuid', 1)], unique=True)