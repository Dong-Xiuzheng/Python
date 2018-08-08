#!/usr/bin/python
#coding=utf-8
import os
import sys
import filecmp

def mkdir(my_path):
    my_path=my_path.strip()
    is_exists=os.path.exists(my_path)
    if not is_exists:
        os.makedirs(my_path)
        #print my_path+" create path succss"
    else:
        #print my_path+" already exist"
        os.chdir(my_path)
        files=os.listdir(my_path)
        for file in files:
            os.remove(file)
            #print file+" deleted!"
        os.chdir("..")

def get_key_index(path,filename,key_name):
    srcfile=open(path+"/"+filename)
    line_str=srcfile.readline()
    srcfile.close
    return line_str.strip().split(",").index(key_name)

def get_clint_no_list(path, client_id_list):
    map_file=open(path+"/client_map.csv")
    client_no_list=[]
    map_line=map_file.readline()
    map_line=map_file.readline()
    map_line=map_file.readline()
    while map_line:
        client_id=map_line.strip().split(",")[1]
        #print "get_clint_no_list: client_id "+client_id
        if client_id in client_id_list:
            client_no_list.append(map_line.strip().split(",")[0])
        map_line=map_file.readline()
    map_file.close
    return client_no_list
    
def process_file(path, filename, client_no_list):
    key_index=get_key_index(path, filename, "client_no")
    srcfile=open(path+"/"+filename)
    dstfile=open(os.getcwd()+"/simple_csv/"+filename,"a+")
    line_str=srcfile.readline()
    dstfile.write(line_str)
    #print "process filename: "+filename+" key_index: "+str(key_index)
    if filename=="client_map.csv":
        line_str=srcfile.readline()
        dstfile.write(line_str)
    line_str=srcfile.readline()
    while line_str:
        #print line_str.strip().split(",")
        client_no=line_str.strip().split(",")[key_index]
        if client_no in client_no_list:
            dstfile.write(line_str)
        if filename=="client_map.csv":
            #print "client_no="+client_no
            if client_no=="4294967295":
                dstfile.write(line_str)
        line_str=srcfile.readline()
    srcfile.close
    dstfile.close

if __name__ == '__main__':
    result_path=os.getcwd()+"/simple_csv"
    #创建结果目录
    mkdir(result_path)
    #通过脚本入参获取到客户列表
    client_id_list=sys.argv[2:len(sys.argv)]
    client_no_list=get_clint_no_list(sys.argv[1],client_id_list)
    #print "client_no_list:"
    #print client_no_list
    process_file(sys.argv[1],"client_map.csv", client_no_list)
    process_file(sys.argv[1],"client.csv", client_no_list)
    process_file(sys.argv[1],"client_posi.csv", client_no_list)
    print os.system("pause")