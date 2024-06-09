from typing import Optional,Dict
import typer
from re import search
from parser_log import __appName__ , __version__
from rich.console import Console
from rich.table import Table


app = typer.Typer()
console = Console()



def _version_callback(value : bool) -> None:
    if value:
        print(f"{__appName__} v{__version__}")
        raise typer.Exit()
    

def sortDictInDescOrder(dictionary:Dict) -> Dict:
    return dict(sorted(dictionary.items(),key=lambda x:x[1],reverse=True))


# typer.option( here we can choose what to take as input and also modify default outputs like what to show in help falg )


# * for default vesion

@app.callback()
def main(version : Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show application version and exit",
    callback=_version_callback,
    is_eager="true"
    )
) -> None:
    return


# * default parse command

@app.command()
def parse(filename:str) -> None:

    ipAddresses = {}

    with open(filename) as f:
        try:
            for lines in f:
                ip,details = lines.split(" - - ",1)
                if ip in ipAddresses.keys():
                    ipAddresses[ip] += 1
                else:
                    ipAddresses[ip] = 1 
            sortedIpAddresses = sortDictInDescOrder(ipAddresses)
            table = Table("ip Addresses","Calls")
            

            for i in sortedIpAddresses.items():
                table.add_row(str(i[0]),str(i[1]))

            console.print(table)    

        except :
            print("error occured")



   

@app.command()
def selective_parse(
    filename : str,
    ip : str = "",
    code : str = ""
    

):  
    if(ip != ""):

        ipTable = Table("ip","time","method","url","response code")

        with open(filename) as f:
            try:
                for lines in f:
                    ip_addresses,details = lines.split(" - - [",1)
                    # if ip not in ip_addresses:
                    #     print("ip addresses not found")
                    #     return
                    if ip == ip_addresses:
                        
                        time , urlAndMethd = details.split("] \"",1)
                        
                        method , url = urlAndMethd.split(" ",1)
                        
                        urlAddress,statusCode = url.split("\" ",1)

                        responseCode,responseTIme = statusCode.split(" ",1)
                        
                        if(code != "" and code == responseCode):
                            ipTable.add_row(ip_addresses,time,method,urlAddress,responseCode)

                        elif(code == ""):
                            ipTable.add_row(ip_addresses,time,method,urlAddress,responseCode)
                            
                if ip_addresses != " ": 
                    console.print(ipTable)
                else:
                    print("ip addresses not found")    

            except:
                print("error occured")            
    elif(ip == ""):
        print("please enter a valid ip addresses")            