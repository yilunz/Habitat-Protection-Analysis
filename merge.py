import arcpy, os,fnmatch

input_bird=r"D:/test_revise/output_second/summary_dbf_1/bird"
input_mammal=r"D:/test_revise/output_second/summary_dbf_1/mammal"
output=r"D:/test_revise/output_second/summary"

def merge_dbf(input_animal,output):
    animal_name=input_animal.split("/")[4]
    print animal_name
    output_root=os.path.join(output,animal_name)
    if not os.path.exists(output_root):
        os.mkdir(output_root)
    else:
        pass
    print output_root
    
    
    ts=os.listdir(input_animal)
    print ts
    for t in ts:
        t_path=os.path.join(input_animal,t)
        ps=os.listdir(t_path)
        print ps

        output_t=os.path.join(output_root,t)
        if not os.path.exists(output_t):
            os.mkdir(output_t)
        else:
            pass
        print output_t



        for p in ps:
            p_path=os.path.join(t_path,p)
            output_p=os.path.join(output_t,p)
            if not os.path.exists(output_p):
                os.mkdir(output_p)
            else:
                pass
            
            files=os.listdir(p_path)
            arcpy.env.workspace=p_path
            #dbf_files=fnmatch.filter(files,".dbf")
            listTables=arcpy.ListTables()
            #print listTables

            #for table in :
                #list.append(f)
            output_feature="{0}_{1}".format(animal_name,p)+".dbf"
            output_path=os.path.join(output_p,output_feature)
            arcpy.Merge_management(listTables,output_path)


#merge_dbf(input_mammal,output)
merge_dbf(input_bird,output)
