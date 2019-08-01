import os
from glob import glob
import subprocess as sp
import ctypes, sys,time

class PowerShell:
    # from scapy
    def __init__(self, coding, ):
        cmd = [self._where('PowerShell.exe'),
               "-NoLogo", "-NonInteractive",  # Do not print headers
               "-Command", "-"]  # Listen commands from stdin
        startupinfo = sp.STARTUPINFO()
        startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
        self.popen = sp.Popen(cmd, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.STDOUT, startupinfo=startupinfo)
        self.coding = coding

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.popen.kill()

    def run(self, cmd, timeout=15):
        b_cmd = cmd.encode(encoding=self.coding)
        try:
            b_outs, errs = self.popen.communicate(b_cmd, timeout=timeout)
        except sp.TimeoutExpired:
            self.popen.kill()
            b_outs, errs = self.popen.communicate()
        outs = b_outs.decode(encoding=self.coding)
        return outs, errs

    @staticmethod
    def _where(filename, dirs=None, env="PATH"):
        """Find file in current dir, in deep_lookup cache or in system path"""
        if dirs is None:
            dirs = []
        if not isinstance(dirs, list):
            dirs = [dirs]
        if glob(filename):
            return filename
        paths = [os.curdir] + os.environ[env].split(os.path.pathsep) + dirs
        try:
            return next(os.path.normpath(match)
                        for path in paths
                        for match in glob(os.path.join(path, filename))
                        if match)
        except (StopIteration, RuntimeError):
            raise IOError("File not found: %s" % filename)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def count_time(t):
    while(t>0):
        t_out = ' '+str(t) if t<10 else str(t)
        print('\r倒计时:  {:>}'.format(t_out), end='',flush=True)
        time.sleep(1)
        t-=1





if is_admin():
    s = 999
    while s !='0':
        s = input(
'''
=====================================
请选择要进行的操作：
0---->退出
1---->永久关闭ipv6
2---->定时关闭ipv6
3---->开启ipv6
=====================================\n
'''
        )

        # print(type(s))

        if s=='1':
            print('关闭ipv6')
            with PowerShell('GBK') as ps:
                outs, errs = ps.run('Disable-NetAdapterBinding -Name 以太网 -ComponentID ms_tcpip6 -PassThru')
                print('error:', os.linesep, errs)
                print('output:', os.linesep, outs)
            print('ipv6已关闭\n\n') 
        if s=='2':
            t = int(input('临时关闭多少秒？'))
            with PowerShell('GBK') as ps:
                outs, errs = ps.run('Disable-NetAdapterBinding -Name 以太网 -ComponentID ms_tcpip6 -PassThru')
                print('error:', os.linesep, errs)
                print('output:', os.linesep, outs)
                print('ipv6已关闭\n\n') 
            
            count_time(t)                

            with PowerShell('GBK') as ps:
                outs, errs = ps.run('Enable-NetAdapterBinding -Name 以太网 -ComponentID ms_tcpip6 -PassThru')
                print('error:', os.linesep, errs)
                print('output:', os.linesep, outs)
            print('ipv6已开启\n\n') 
            time.sleep(2)
            s = '0'
        if s=='3':
            with PowerShell('GBK') as ps:
                outs, errs = ps.run('Enable-NetAdapterBinding -Name 以太网 -ComponentID ms_tcpip6 -PassThru')
                print('error:', os.linesep, errs)
                print('output:', os.linesep, outs)
            print('ipv6已开启\n\n') 
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:#in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

