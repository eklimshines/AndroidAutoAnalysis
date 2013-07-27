import optparse
import os
import zipfile
import shutil

p = optparse.OptionParser()
p.add_option("-d", action="store",dest="dst", help = "destionation dir")
p.add_option("-s", action="store",dest="source", help = "source file")

p.set_defaults(dst="data")

opts, args = p.parse_args()

srcfile = opts.source
dstdir = opts.dst

#if not os.path.isdir(dstdir):
#    os.mkdir(dstdir)
getdir = os.getcwd()

shutil.copy(srcfile, getdir+"/lib/android.apk")

#apk unzip
os.chdir("./lib")

if dstdir == "data":
    os.system("java -jar apktool.jar d android.apk ../data")
else:
    os.system("java -jar apktool.jar d android.apk " + dstdir)

os.chdir(getdir)

zipl = dstdir+"/zip"

z = zipfile.ZipFile(srcfile,"r")
z.extractall(zipl)
z.close()

shutil.copy(zipl+"/classes.dex", dstdir+"/classes.dex")

#java –jar baksmli-1.4.2.jar –o ./ classes.dex
#java -jar ddx.jar -d <directory> <dex file>

#os.system("java -jar ./lib/baksmali.jar -o " + dstdir+"/smali " + dstdir +"/classes.dex")
os.system("java -jar ./lib/ddx.jar -d " + dstdir + "/ddx " + dstdir +"/classes.dex")

#print ("now dir ..." + getdir)

#dex -> jar
os.chdir("./lib/dex2jar")

if dstdir == "data":
    os.system("dex2jar " +"../../data/classes.dex")
else:
    os.system("dex2jar " + dstdir +"/classes.dex")
    
os.chdir(getdir)

#jar -> java

classpath = dstdir+"/class"

#if not os.path.isdir(classpath):
#    os.mkdir(classpath)

z = zipfile.ZipFile(dstdir+"/classes_dex2jar.jar","r")
z.extractall(classpath)
z.close()

#jad -o -r -sjava -d./src classes/**/*.class
os.chdir("./lib/jad")

if dstdir == "data":
    os.system("jad -o -r -sjava -d ../../data/src ../../data/class/**/*.class")
else:
    os.system("jad -o -r -sjava -d "+ dstdir +"/src "+ dstdir + "/**/*.class")

os.chdir(getdir)
