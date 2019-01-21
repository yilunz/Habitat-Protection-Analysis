import arcpy, os, fnmatch, pandas, numpy, csv
mammal_input=r"D:\test_revise\mammal_input"
bird_input=r"D:\test_revise\bird_input"
amphibian_input=r"D:\test_revise\amphibian_input"
#preserve_area=r"C:\Users\zyilun\Desktop\test_revise\output\preserve_area"
output=r"D:\test_revise\output"

def select(animal_input, output):
    animal_folders=os.listdir(animal_input)
    animal_output_root_name=animal_folders[0]
    animal_type=animal_output_root_name.split("_")[0]

    #head=["Species range/NNR", "<10","10-100","100-1000","1000-10000",
          #"10000-100000",">100000"]
    animal_range=["0","10","100","1000","10000","100000"]

    #build animal_output folder:
    animal_outputs_root=os.path.join(output,animal_type)
    if not os.path.exists(animal_outputs_root):
        os.mkdir(animal_outputs_root) #output\mammal


    #intersect_outputs_root=os.path.join(output,"intersect")
    #if not os.path.exists(intersect_outputs_root):
        #os.mkdir(intersect_outputs_root)


    #output_csv_root=os.path.join(output,"tables") #output\mammal\tables

    #if not os.path.exists(output_csv_root):
        #os.mkdir(output_csv_root)

    animals=fnmatch.filter(animal_folders,"*.shp") 
    for a in animals:
        a_name=a.split(".")[0]
        a_path=os.path.join(animal_input,a)
        animal_output_path=os.path.join(animal_outputs_root,a_name) #output\mammal\mammal_china
        #select_output_path=os.path.join(animal_output_path,"select")#output\mammal\mammal_china\select
        #intersect_output_path=os.path.join(animal_output_path,"intersect")#output\mammal\mammal_china\intersect
                    
        if not os.path.exists(animal_output_path):
            os.mkdir(animal_output_path)

        #if not os.path.exists(select_output_path):
            #os.mkdir(select_output_path)

        #if not os.path.exists(intersect_output_path):
            #os.mkdir(intersect_output_path)

                    
        for r in range(len(animal_range)):
            if r==5:
                #print animal_range[r]
                expression="""{0}>{1}""".format(arcpy.AddFieldDelimiters(a_path,"Area_km2"),animal_range[r])
                #print expression
                select_output_feature="{0}_{1}_{2}".format(animal_range[r],"higher",a_name)+".shp"
                #select_output_feature_path=os.path.join(select_output_path,select_output_feature)
            else:
                #print animal_range[r]
                expression="""{0}>{1} AND {2}<={3}""".format(arcpy.AddFieldDelimiters(a_path,"Area_km2"),animal_range[r],
                                                                         arcpy.AddFieldDelimiters(a_path,"Area_km2"),animal_range[r+1])
                #print expression
                select_output_feature="{0}_{1}_{2}".format(animal_range[r],animal_range[r+1],a_name)+".shp"
                            

            #select base on expression
            select_output_feature_path=os.path.join(animal_output_path,select_output_feature)
            select_output_feature_name=select_output_feature.split(".")[0]
            arcpy.Select_analysis(a_path,select_output_feature_path,expression)


   
            

select(mammal_input,output)   
                    
    
