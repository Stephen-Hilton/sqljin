from datetime import date, datetime, timedelta
from pathlib import Path 
import shutil
from sys import api_version
from numpy import append 
import pandas as pd 


class format_date_in_file():
    csvfilepath: Path = None 
    columns: list = None 
    utils: dict = None 
    headerrow: bool = None
    input_dateformatstring: str = None 
    input_dateformat: dict = None 
    output_dateformatstring: str = None 
    output_dateformat: dict = None 
    # dateformat: dict = None 


    # Initiate Class:
    def __init__(self, **kwargs) -> None:

        self.starttime = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
        self.log = print
        self.utils = self.first_arg_found(kwargs, ['utils'])
        if self.utils and type(self.utils)==dict and 'log' in self.utils.keys():
            self.log = self.utils['log']
            
        self.log(f'format_date_in_file started - starttime: {self.starttime}')
        self.csvfilepath = Path(self.first_arg_found(kwargs, ['path','filepath','csvfilepath','csvfile','csvpath']))
        self.columns = list(self.first_arg_found(kwargs, ['columns','column','cols','col']))
        self.headerrow = bool(self.first_arg_found(kwargs, ['headers','head','header_flag','headerflag'], True))
        self.input_dateformatstring = str(self.first_arg_found(kwargs,  ['input_dateformatstring','inputdateformat','input_date_format'], 'm/d/y  h:m:s'))
        self.output_dateformatstring = str(self.first_arg_found(kwargs,  ['output_dateformat','outputdateformat','output_date_format'], 'yyyy-mm-dd hh:mm:ss'))

        self.input_dateformat  = self.digest_dateformat_string(self.input_dateformatstring)
        self.output_dateformat = self.digest_dateformat_string(self.output_dateformatstring)
            

    # ------------------------------
    #  Required Classes from ABC
    # ------------------------------

    def execute(self, csvfilepath:Path=None):

        if not csvfilepath: csvfilepath = self.csvfilepath

        # make copy of original, just for saftey:
        oldcsvfilepath = Path(str(csvfilepath.resolve())[:-4] + '---backup.csv')
        if not oldcsvfilepath.exists():
            shutil.copy(csvfilepath, oldcsvfilepath)
        
        # load csv into dataframe
        df = pd.read_csv(csvfilepath.resolve())

        # modify all requested date columns
        for col in self.columns:
            df.iloc[:, col] = df.iloc[:, col].apply(self.apply_dateformat)

        # save .csv
        df.to_csv(self.csvfilepath, index=False)
        return None




    def apply_dateformat(self, datetimevalue:str) -> str:
        """apply the date format transformation from the digested input format to the TD standard output format

        Args:
            datetimevalue (str): actual date/timevalue to transform

        Returns:
            str: transformed date/time value
        """
        self.log(f'   was: {datetimevalue}')
        newdatevalue = newtimevalue = ''
        pos = self.input_dateformat
        datetime_array = datetimevalue.split( pos['datetime delim'])
        datefound = timefound = False
        for _arypart in datetime_array:
            if pos['date delim'] in _arypart:
                date_array = _arypart.split(pos['date delim'])
                date  = str(date_array[pos['date']]).rjust(2,'0')
                month = str(date_array[pos['month']]).rjust(2,'0')
                year  = str(date_array[pos['year']])
                if len(year) == 2: year = f'20{year}'
                newdatevalue = f'{year}-{month}-{date}'
                datefound = True 
            if pos['time delim'] in _arypart:
                time_array = _arypart.split(pos['time delim'])
                hour   = str(time_array[pos['hour']]).rjust(2,'0') 
                minute = str(time_array[pos['minute']]).rjust(2,'0') if len(time_array) >= 2 else '00'
                second = str(time_array[pos['second']]).rjust(2,'0') if len(time_array) >= 3 else '00'
                newtimevalue = f'{hour}:{minute}:{second}'
                timefound = True 

        # put them together:
        if datefound and timefound:  
            dt = datetime(year,month,date,hour,minute,second)
        elif datefound:
            dt = datetime(year,month,date)
        elif timefound:
            dt = datetime(hour=hour, minute=minute, second=second)
        else:
            dt = None 
        
        if dt:
            newdatetimevalue = dt.strftime(self.output_dateformat['strftime'])
        else:
            newdatetimevalue = f'{newdatevalue} {newtimevalue}'.strip()
        self.log(f'   now: {newdatetimevalue}')
        return newdatetimevalue




    def digest_dateformat_string(self, input_dateformatstring:str) -> dict:
        date_delims =  ['/','-','.','_','\\']
        time_delims =  [':']
        datetime_delims = [' ']
        rtn = {'raw': input_dateformatstring}
        input_dateformatstring = self.remove_extra_spaces(input_dateformatstring).lower()
        rtn['original'] = input_dateformatstring

        # build dateformat string array:
        for _delim in datetime_delims:
            if _delim in input_dateformatstring:
                datetime_array = input_dateformatstring.split(_delim)
                rtn['datetime delim'] = _delim 
                break
        if not datetime_array: datetime_array = [input_dateformatstring]

        # determine what parts of the dateformat array is date, time, or both
        if len(datetime_array) == 2:  # assumption: Date always comes before Time
            rtn['date original'] = datetime_array[0].strip()
            for _delim in date_delims:
                if _delim in rtn['date original']:
                    rtn['date delim'] = _delim 
                    break
            rtn['time original'] = datetime_array[1].strip()
            for _delim in time_delims:
                if _delim in rtn['time original']:
                    rtn['time delim'] = _delim 
                    break

        elif len(datetime_array) == 1:
            for _arypart in datetime_array:    
                for _delim in date_delims:
                    if _delim in _arypart:
                        rtn['date original'] = _arypart.strip()
                        rtn['date delim'] = _delim 
                        break
                for _delim in time_delims:
                    if _delim in _arypart:
                        rtn['time original'] = _arypart.strip()
                        rtn['time delim'] = _delim 
                        break
        else:
            raise TypeError("supplied date format string was invalid")
            
        # at this point, should have valid date/time or both:
        date_strftime = []
        if 'date original' in rtn:
            for ipos, _datepart in enumerate(rtn['date original'].split(rtn['date delim'])):
                if 'd' in _datepart:  
                    rtn['date'] = ipos 
                    date_strftime.append('%-d') if len(_datepart)==1 else date_strftime.append('%d')
                if 'y' in _datepart:  
                    rtn['year'] = ipos 
                    date_strftime.append('%Y') if len(_datepart)>=3 else date_strftime.append('%y')
                if 'm' in _datepart:  
                    rtn['month'] = ipos 
                    date_strftime.append('%-m') if len(_datepart)==1 else date_strftime.append('%m')

        time_strftime = []
        if 'time original' in rtn:
            for ipos, _datepart in enumerate(rtn['time original'].split(rtn['time delim'])):
                if 'h' in _datepart:  
                    rtn['hour'] = ipos 
                    time_strftime.append('%-H') if len(_datepart)==1 else time_strftime.append('%H')
                if 'm' in _datepart:  
                    rtn['minute'] = ipos 
                    time_strftime.append('%-M') if len(_datepart)==1 else time_strftime.append('%M')
                if 's' in _datepart:  
                    rtn['second'] = ipos 
                    time_strftime.append('%-S') if len(_datepart)==1 else time_strftime.append('%S')

        # add python datetime string format strftime()
        rtn['strftime'] = str(rtn['date delim']).join(date_strftime) + rtn['datetime delim'] + str(rtn['time delim']).join(time_strftime)
        return rtn 



    def remove_extra_spaces(self, string:str) -> str:
        """reduces all extra spaces inside a string to a single space

        Args:
            string (str): any string value

        Returns:
            str: string value with multiple spaces replaced with a single space
        """
        while True:
            if '  ' in string: 
                string = string.replace('  ',' ')
            else:
                break
        return string.strip()



    def first_arg_found(self, arg_dict:dict, valid_name_list:list, default:str=None):
        """returns the first value that matches between valid_name_list and the arg_dict.keys

        Args:
            valid_name_list (list): list of valid keys to return from the arg_dict
            arg_dict (dict): kwargs dictionary to attempt to match from valid_name_list
            default (str): default value to return if not found

        Returns:
            any: the first value from arg_dict that matches anything in valid_name_list, or default | None if not found
        """
        for valid_name in valid_name_list:
            if valid_name in arg_dict.keys():
                val = arg_dict[valid_name]
                self.log(f'variable found: {valid_name} = {str(val)}')
                return val
        self.log(f'variable not found for any: {valid_name_list} -- defaults to "{default}"')
        return default







if __name__ == '__main__':
    #proc = format_date_in_file(filepath=Path('steps') / 'gssresusage_override -- MENARDS7 -- 2022-02-15 to 2022-02-20.csv', columns=[4,7])
    #proc.execute()


    def remove_extra_spaces(string:str) -> str:
        """reduces all extra spaces inside a string to a single space

        Args:
            string (str): any string value

        Returns:
            str: string value with multiple spaces replaced with a single space
        """
        while True:
            if '  ' in string: 
                string = string.replace('  ',' ')
            else:
                break
        return string.strip()


    def translate_simple_dateformat(input_dateformat:str) -> str:
        """Translates a simplified date format into python strftime format, for consumption in datetime.datetime. 
        Simplified format will visually look similar to the final output, and is useful for bridging between MSOffice and Python. 
        Also performs context-specific classification of shared characters, such as "m" for both month and minute.  
        For example, supplying  yyyy-mm-dd hh:mm:dd  will work as expected, using the context of characters surrounding the "m" 
        to interpret between Month and Minute.  

        Args:
            input_dateformat (str): simplified format string (i.e.,  yyyy-mm-dd hh:mm:ss )

        Returns:
            str: format string compatible with datetime.datetime.strftime() functions
        """
        oldfmt = str(remove_extra_spaces(input_dateformat)).lower()
        oldfmt = oldfmt.replace('12hh','ii').replace('12h','i').replace('24h','h').replace('excel','m/d/yy i:m:s p').lower()
        charlist = []
        date_markers = ['y','d','/','-','w']
        time_markers = ['h','s',':','i','p','a']
        both_markers = ['m']

        # iterate each character of format, and assign a type (date/time/unknown)
        prev_chardict = {}
        repeat = 0
        for i, c in enumerate(oldfmt):  
            ctype = None 

            if c in date_markers: ctype = 'd'
            if c in time_markers: ctype = 't'
            if c in both_markers:  # use context of surrounding characters
                ctype = None 
                # Oscillate forward and backward until we find the next closest valid value:
                for o in range(1, len(oldfmt)):
                    at_beginning = bool(((i-o) < 0))
                    at_end = bool(i+o == len(oldfmt))
                    if not at_beginning: # look behind unless at beginning of string
                        oc = oldfmt[i+(o*-1): i+1+(o*-1)]
                        if oc in date_markers: ctype = 'd'
                        if oc in time_markers: ctype = 't'
                    if not ctype and not at_end:  # look ahead unless found, or at end of string
                        oc = oldfmt[i+o: i+1+o]
                        if oc in date_markers: ctype = 'd'
                        if oc in time_markers: ctype = 't'
                    if ctype: break 

            if not ctype: ctype = 'u'
            chardict = {'char':c, 'type':ctype}

            # track / collapse repeating characters
            if prev_chardict != {} and f'{chardict["char"]}--{chardict["type"]}' == f'{prev_chardict["char"]}--{prev_chardict["type"]}': 
                prev_chardict['repeat'] +=1
            else:
                chardict['repeat'] = 1
                charlist.append(chardict)
                prev_chardict = chardict 

        # final translation of characters into strftime format
        fmt = []
        for c in charlist:
            cd = ''
            if   c['type'] == 't':
                if   c['char'] == 'h': 
                    if   c['repeat'] ==1: cd = '%-H'
                    elif c['repeat'] >=2: cd = '%H'
                elif c['char'] == 'i': 
                    if   c['repeat'] ==1: cd = '%-I'
                    elif c['repeat'] >=2: cd = '%I'
                elif c['char'] == 'm': 
                    if   c['repeat'] ==1: cd = '%-M'
                    elif c['repeat'] >=2: cd = '%M'
                elif c['char'] == 's': 
                    if   c['repeat'] ==1: cd = '%-S'
                    elif c['repeat'] >=2: cd = '%S'
                elif c['char'] in ['a','p']: cd = '%p' # am/pm

            elif c['type'] == 'd':
                if   c['char'] == 'y': 
                    if   c['repeat'] <=2: cd = '%y'
                    elif c['repeat'] >=3: cd = '%Y'
                elif c['char'] == 'm': 
                    if   c['repeat'] ==1: cd = '%-m'
                    elif c['repeat'] ==2: cd = '%m'
                    elif c['repeat'] ==3: cd = '%b'
                    elif c['repeat'] >=4: cd = '%B'
                elif c['char'] == 'w': 
                    if   c['repeat'] ==1: cd = '%w'
                    elif c['repeat'] ==2: cd = '0%w'
                    elif c['repeat'] >=3: cd = '%W'
                elif c['char'] == 'd': 
                    if   c['repeat'] ==1: cd = '%-d'
                    elif c['repeat'] ==2: cd = '%d'
                    elif c['repeat'] ==3: cd = '%a'
                    elif c['repeat'] >=4: cd = '%A'            
            if cd == '': 
                cd = str(c['char']) * int(c['repeat'])
            fmt.append(cd)
        return ''.join(fmt).strip()




    for fmt in ['m/d/yy h:m:s', 'yyyy-mm-dd hh:mm:ss', 'mm/dd/yyyy', 'hh:mm:ss', 'yyyymmdd_hhmmss', 'Excel', '24hh == 12hhp']:
        oldfmt = fmt.rjust(20,' ')
        newfmt = translate_simple_dateformat(fmt)
        nowish = datetime.now()
        print(f'from {oldfmt}   to   {newfmt.ljust(25," ")}  looks like { nowish.strftime(newfmt)}')
