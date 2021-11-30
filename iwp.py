


class IWP:
    """
    Class to read, parse and save as TXT file a given IWP file used in
    OLIVETTI JetWriter 900 and compatible typewriter devices.
    """
    name = None
    raw_data = ''
    raw_data_len = 0
    enc_data = ''
    enc_data_len = 0
    debug = True

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

        pos = -1
        state='idle'
        skip_count=0
        for ch in self.raw_data[self.doc_begin_idx:-1]:
            pos += 1
            if ch == 0x0d:
                ch = '\n'
            elif ch == 0x00:
                continue
            if self.debug is True:
                try:
                  print("0x%04x: [%3d] %12s '%c'" % (pos, ch, state, ch))
                except:
                  print("0x%04x: [???] %12s '?'" % (pos, state))
            if ch == 0x06:
                state = 'skip_06_code'
                skip_count = 2
                continue
            elif ch == 0x07:
                state = 'skip_07_code'
                skip_count = 2
                continue
            elif ch == 0x08:
                state = 'skip_08_code'
                skip_count = 2
                continue
            elif ch == 0x05:
                state = 'skip_05_code'
                skip_count = 2
                continue

            if state == 'idle':
                self.enc_data += "%c" % ch  
            elif state == 'skip_06_code':
                skip_count-=1
                if skip_count == 1:
                    if ch in [0x8e,]:
                      ch = 0x0a # \n
                    else:
                      ch = 0x20 # SPACE
                    self.enc_data += "%c" % ch
                elif skip_count == 0:
                    state = 'idle'
            elif state == 'skip_07_code':
                skip_count-=1
                #if skip_count == 1:
                #    if ch in [0x80, 0x8e, 0x8f]:
                #        self.enc_data += '\n'
                if skip_count == 0:
                    state = 'idle'
            elif state == 'skip_08_code':
                skip_count-=1 
                if skip_count == 1:
                    if ch in [0x80, 0x8e, 0x8f]:
                        self.enc_data += '\n'
                if skip_count == 0:
                    state = 'idle'
            elif state == 'skip_05_code':
                skip_count -= 1
                if skip_count == 0:
                    self.enc_data += '\n'
                    state = 'idle'
            else:
                print("ERROR: Unhandled state: %s" % state)
        self.enc_data_len = len(self.raw_data)
        print("Encoded data length: '%d'" % self.enc_data_len)

    def save(self, **kwargs):
        name = kwargs.get('name', None)
        if name is None:
            print("ERROR: TXT file not specified")
            return False
        try:
            f=open(name, 'wt')
            f.write(self.enc_data)
            f.close()
        except:
            print("ERROR: Unable to write file '%s'" % name)
            return 1
        print("Written file: '%s' (%d bytes)" % (name, self.enc_data_len))
        return 0   

iwp_file = 'iwp/PRESENT.IWP'
#iwp_file = 'iwp/ALBANES.IWP'
txt_file = iwp_file[0:-3] + 'txt'

iwp = IWP(name=iwp_file)
iwp.load()
iwp.parse()
print("RAW")
print(iwp.raw_data)
print("ENC")
print(iwp.enc_data)
iwp.save(name=txt_file)

