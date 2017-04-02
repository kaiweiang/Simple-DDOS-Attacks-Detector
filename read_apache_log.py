def apache_log_row(fo):
    ''' 
    Fast split on Apache2 log lines
    http://httpd.apache.org/docs/trunk/logs.html
    source: http://stackoverflow.com/questions/12544510/parsing-apache-log-files
    '''
    while True:
        s = next(fo)
        row = [ ]
        qe = qp = None # quote end character (qe) and quote parts (qp)
        for s in s.replace('\r','').replace('\n','').split(' '):
            if qp:
                qp.append(s)
            elif '' == s: # blanks
                row.append('')
            elif '"' == s[0]: # begin " quote "
                qp = [ s ]
                qe = '"'
            elif '[' == s[0]: # begin [ quote ]
                qp = [ s ]
                qe = ']'
            else:
                row.append(s)
            l = len(s)
            if l and qe == s[-1]: # end quote
                if l == 1 or s[-2] != '\\': # don't end on escaped quotes
                    row.append(' '.join(qp)[1:-1].replace('\\'+qe, qe))
                    qp = qe = None
        yield row
