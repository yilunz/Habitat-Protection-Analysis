require(gdata)

################################ Import tables ################################
# mammal build data
mammal0build=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_0_1979_BuildTime.xls",sheet=1,header=T)
mb1=mammal0build[c(1:7)]
mb2=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_1979_2000_BuildTime.xls",sheet=1,header=T)
mb3=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_2000_later_BuildTime.xls",sheet=1,header=T)

# mammal promote data
mp1=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_0_1979_PromoteTime.xls",sheet=1,header=T)
mp2=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_1979_2000_PromoteTime.xls",sheet=1,header=T)
mp3=read.xls("/Users/jacaranda/Desktop/output_second/mammal/mammal_2000_later_PromoteTime.xls",sheet=1,header=T)

# bird build data
bb1=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_0_1979_BuildTime_clean.xls"
             ,sheet = 1,header=T)
bb2=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_1979_2000_BuildTime_clean.xls",
             sheet=1,header=T)
bb3=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_2000_later_BuildTime_clean.xls",
             sheet=1,header=T)

# bird promote data
bp1=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_0_1979_PromoteTime_clean.xls",
             sheet=1,header=T)
bp2=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_1979_2000_PromoteTime_clean.xls",
             sheet=1,header=T)
bp3=read.xls("/Users/jacaranda/Desktop/output_second/bird/bird_2000_later_PromoteTime_clean.xls",
             sheet=1,header=T)

# amphibian build data
ab1=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/0_1979_build_amphibian_final.xls",
              sheet = 1,header=T)
ab2=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/1979_2000_build_amphibian_final.xls",
             sheet = 1,header=T)
ab3=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/2000_later_build_amphibian_final.xls",
             sheet = 1,header=T)

# amphibian promote data
ap1=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/0_1979_promote_amphibian_final.xls",
             sheet = 1,header=T)
ap2=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/1979_2000_promote_amphibian_final.xls",
             sheet = 1,header=T)
ap3=read.xls("/Users/jacaranda/Desktop/output_second/amphibian/2000_later_promote_amphibian_final.xls",
             sheet = 1,header=T)


#### Function for calculate mean protected percentage of each habitat range ####

size=c(0,10,100,1000,10000,100000,1000000)
rowName=c("0-10","10-100","100-1,000","1,000-10,000","10,000-100,000","100,000-1,000,000","1,000,000- higher")

calculate_meanPer<-function(df){
  df$proPer=df$Protected_Area/df$Habitat_Area
  bmean=c()
  for (j in 1:length(size)) {
    if(j<7){
      b=subset(df,Habitat_Area>=size[j]&Habitat_Area<size[j+1])
      bmean[j]=mean(b$proPer)
      j=j+1
    }else{
      b=subset(df,Habitat_Area>=size[j])
      bmean[j]=mean(b$proPer)
      j=j+1
    }
    
  }
  return(bmean)
}

######################## replace Na values and add row names ####################

mbuild1=calculate_meanPer(mb1)
mbuild2=calculate_meanPer(mb2)
mbuild3=calculate_meanPer(mb3)
mammalbuild=data.frame(cbind(mbuild1,mbuild2,mbuild3))
row.names(mammalbuild)=rowName
mammalbuild[is.na(mammalbuild)]=0

mpromote1=calculate_meanPer(mp1)
mpromote2=calculate_meanPer(mp2)
mpromote3=calculate_meanPer(mp3)
mammalpromote=data.frame(cbind(mpromote1,mpromote2,mpromote3))
row.names(mammalpromote)=rowName
mammalpromote[is.na(mammalpromote)]=0

bbuild1=calculate_meanPer(bb1)
bbuild2=calculate_meanPer(bb2)
bbuild3=calculate_meanPer(bb3)
birdbuild=data.frame(cbind(bbuild1,bbuild2,bbuild3))
row.names(birdbuild)=rowName
birdbuild[is.na(birdbuild)]=0

bpromote1=calculate_meanPer(bp1)
bpromote2=calculate_meanPer(bp2)
bpromote3=calculate_meanPer(bp3)
birdpromote=data.frame(cbind(bpromote1,bpromote2,bpromote3))
row.names(birdpromote)=rowName
birdpromote[is.na(birdpromote)]=0

abuild1=calculate_meanPer(ab1)
abuild2=calculate_meanPer(ab2)
abuild3=calculate_meanPer(ab3)
amphibianbuild=data.frame(cbind(abuild1,abuild2,abuild3))
row.names(amphibianbuild)=rowName
amphibianbuild[is.na(amphibianbuild)]=0

apromote1=calculate_meanPer(ap1)
apromote2=calculate_meanPer(ap2)
apromote3=calculate_meanPer(ap3)
amphibianpromote=data.frame(cbind(apromote1,apromote2,apromote3))
row.names(amphibianpromote)=rowName
amphibianpromote[is.na(amphibianpromote)]=0





######################## Function for making figures #########################

require(ggplot2)
library(scales)
library(grid)
library(RColorBrewer)
#plot(mammalbuild)

make_figure<-function(df,df1,df2,df3,animal){
  a=ggplot(data=df)
  a+geom_point(aes(x=row.names(df),y=df[,1]),color="#66c2a5",
               size=2,shape=1)+
    geom_point(aes(x=row.names(df),y=df[,2]),color="#fc8d62",
               size=2,shape=1)+
    geom_point(aes(x=row.names(df),y=df[,3]),color="#8da0cb",
               size=2,shape=1)+
    ylab("Average Protected Percentage")+
    theme_classic()+
    theme(axis.text.x = element_text(angle = 45, hjust = 1,size=10),
          axis.text.y = element_text(size=10),
          axis.ticks = element_blank())+
    geom_hline(yintercept=(sum(df1$Protected_Area)/sum(df1$Habitat_Area)),
               linetype="dashed",color="#66c2a5") +
    geom_hline(yintercept=(sum(df2$Protected_Area)/sum(df2$Habitat_Area)),
               linetype="dashed",color="#fc8d62")+
    geom_hline(yintercept=(sum(df3$Protected_Area)/sum(df3$Habitat_Area)),
               linetype="dashed",color="#8da0cb")+
    scale_y_continuous(limits=c(0,1),breaks=seq(0,1,0.2),labels = percent)+
    scale_x_discrete(name ="Habitat Range", 
                     limits=rowName)+
    geom_text(x=6, y=0.9, label=animal,size=5)
}

make_figure(mammalbuild,mb1,mb2,mb3,"Mammals")
make_figure(mammalpromote,mp1,mp2,mp3,"Mammals")
make_figure(birdbuild,bb1,bb2,bb3,"Birds")
make_figure(birdpromote,bp1,bp2,bp3,"Birds")

make_figure(amphibianbuild,ab1,ab2,ab3,"Amphibians")
make_figure(amphibianpromote,ap1,ap2,ap3,"Amphibians")








