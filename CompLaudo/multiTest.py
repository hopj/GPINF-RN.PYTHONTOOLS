import multiprocessing
import sys
 
def printString(nome):
    return nome+"-thread"
 
  
if __name__ == '__main__':   
    pool = multiprocessing.Pool(4)
    try: 
        r = [pool.apply_async(printString, args=(str1,)) for str1 in ["galileu", "hamilton", "bruno", "peron"]]
        output = [p.get(timeout=10) for p in r]
        for n in output:
            print (str(n))
        pool.terminate()
    except :
        print("Unexpected error:", sys.exc_info())