# ASCII Object Model:
# 
# sqljin_guirunner --|
#                    |
# sqljin_guieditor --|--- startup ---|
#                    |               |- logger 
# sqljin_cli --------|               |- util   
#                                    |- event  
#                                    |- config  
#                                    |- update  
#                                    |- objects ---|
#                                                  |- collections -- processes -- steps -- tasks
#                                                  |- systems
#                                                  |- history
#                                                  |- variables
                                           

from utils import util 

print(util.find_first(['my','test','list'], {'test':'winner','list':'looser'}))

if __name__ == '__main__':
    print('go!')