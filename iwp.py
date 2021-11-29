


class IWP:

    name = None
    raw_data = ''
    raw_data_len = 0
    enc_data = ''


    doc_begin = b'\xf6\x9f\x05\x99\xa0'
    

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)

    def load(self):
        if self.name is None:
            print("ERROR: IWP file not specified")
            return False
        try:
            f=open(self.name, 'rb')
            self.raw_data=f.read()
            f.close()
        except:
            print("ERROR: Unable to read file '%s'" % self.name)
            return 1
        self.raw_data_len = len(self.raw_data)
        print("Loaded: '%s' (%d bytes)" % (self.name, self.raw_data_len))
        return 0

    def parse(self):
        if len(self.raw_data) == 0:
            print("ERROR: No IWP data loaded")
            return False
        self.doc_begin_idx =  self.raw_data.index(self.doc_begin) + len(iwp.doc_begin)
        print("Document begins at: '%d'" % self.doc_begin_idx)

        state='idle'
        skip_count=0
        for ch in self.raw_data[self.doc_begin_idx:-1]:
            if state == 'idle':
                if ch == 0x06:
                    state = 'skip_06_code'
                    skip_count = 2
                    continue
                elif ch == 0x07:
                    state = 'skip_07_code'                    
                    continue
                elif ch == 0x08:
                    state = 'skip_08_code'
                    continue
                elif ch == 0x05:
                    state = 'skip_05_code'
                    skip_count = 2
                elif ch == '\r':
                    ch = '\n'
                self.enc_data += "%c" % ch
            elif state == 'skip_06_code':
                skip_count-=1
                if skip_count == 1:
                    if ch in [0x8e,]:
                      ch = '\n'
                    self.enc_data += ' '
                elif skip_count == 0:
                    state = 'idle'
            elif state == 'skip_07_code':            
                if ch in [0x80, 0x8e,]:
                    self.enc_data += '\n'
                    state = 'idle'
            elif state == 'skip_08_code':            
                if ch in [0x80, 0x8e,]:
                    self.enc_data += '\n'
                    state = 'idle'
            elif state == 'skip_05_code':
                skip_count -= 1
                if skip_count == 0:
                    self.enc_data += '\n'
                    state = 'idle'
            else:
                print("ERROR: Unhandled state: %s" % state)


#iwp = IWP(name='iwp/PRESENT.IWP')
iwp = IWP(name='iwp/ALBANES.IWP')
iwp.load()
iwp.parse()
print("RAW")
print(iwp.raw_data)
print("ENC")
print(iwp.enc_data)

