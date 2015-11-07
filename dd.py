#-*- coding: utf-8 -*-

import os
import sys
import colorama

ERR_ArgsNumber = 1
ERR_DirectNoExist = 2

def Exit(errCode):
    ErrorMsg = {
        ERR_ArgsNumber: '参数错误',
        ERR_DirectNoExist: '目标目录不存在',
    }
    MSG_Usage = '使用方法:dd [目标目录]'
    msg = ErrorMsg.get(errCode, '未知错误')
    print (msg, MSG_Usage, sep='\n')
    sys.exit(1)

def dd_size(destDir):
    for root, dirs, files in os.walk(destDir):
        for subDir in dirs:
            subDirAbs = os.path.join(root, subDir)
            yield (0, subDirAbs, sum([sum([os.stat(os.path.join(root2, subFile2)).st_size for subFile2 in files2]) for root2, dirs2, files2 in os.walk(subDirAbs)]))
        del dirs[:]
        for subFile in files:
            subFileAbs = os.path.join(root, subFile) 
            yield (1, subFileAbs, os.stat(subFileAbs).st_size)

def main(*args):
    if len(args) != 1:
        Exit(ERR_ArgsNumber)
    if not os.path.isdir(args[0]):
        Exit(ERR_DirectNoExist)

    CollectInfos = list(dd_size(args[0]))
    destDirTotalSz = sum([sz for ft, name, sz in CollectInfos])
    for ft, name, sz in CollectInfos:
        print ((colorama.Fore.CYAN if not ft else colorama.Fore.RESET) + os.path.basename(name), end='\t')
        IsBig = True if (sz / destDirTotalSz) >= 0.1 else False
        print ((colorama.Fore.RED if IsBig else colorama.Fore.GREEN) + '{:.2%}'.format(sz / destDirTotalSz), end='\t')
        readableSize = '{0} BYTE'.format(sz) if sz < 1024**1 else ( '{0}KB'.format('%.2f'%(sz/1024)) if sz < 1024**2 else ( '{0}MB'.format('%.2f'%(sz/(1024**2))) if sz < 1024**3 else '{0}GB'.format('%.2f'%(sz/(1024**3)))))
        print ((colorama.Fore.RED if IsBig else colorama.Fore.GREEN) + readableSize)
        


if __name__ == '__main__':
    colorama.init(autoreset=True)
    main(*sys.argv[1:])
