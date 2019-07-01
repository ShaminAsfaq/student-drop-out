/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package csvreader;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;



/**
 *
 * @author shamin
 */
public class CSVReaderExample {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        normalizeGrades("/home/shamin/NetBeansProjects/CSVReader/Files/csestudentsgrades.csv");
        readAndPrint("/home/shamin/NetBeansProjects/CSVReader/Files/normalizedGrades.csv");
        normalizeSections("/home/shamin/NetBeansProjects/CSVReader/Files/offeredsections.csv");
        normalizeInfo("/home/shamin/NetBeansProjects/CSVReader/Files/studentinfo.csv");
                
    }
    
    public static void normalizeInfo(String str){
        String csvFile = str;
        String outFile = "/home/shamin/NetBeansProjects/CSVReader/Files/normalizedInfo.csv";

        CSVReader reader = null;
        List<String[]> data = new ArrayList<String[]>();

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(outFile));

            reader = new CSVReader(new FileReader(csvFile));
            
            String[] line;
            while ((line = reader.readNext()) != null) {
                
                if(line[10].length()==0 || line[11].length()==0 || line[16].length()==0 || line[17].length()==0){
                    continue;
                }
                                
                String gp = line[6];
                if(gp.endsWith("/=") || gp.endsWith("/-")){
                    gp = gp.substring(0, gp.length()-2);
                }
                line[6] = gp;
                
                if(line[11].startsWith("A")==true || line[11].startsWith("B")==true
                        || line[11].startsWith("C")==true || line[11].startsWith("D")==true){
                    
                    String tmp = line[10];
                    line[10] = line[11];
                    line[11] = tmp;
                }
                
                if(line[17].startsWith("A")==true || line[17].startsWith("B")==true
                        || line[17].startsWith("C")==true || line[17].startsWith("D")==true){
                    
                    String tmp = line[16];
                    line[16] = line[17];
                    line[17] = tmp;
                }
                
                
                
                writer.writeNext(line);                
                
            }
            
            writer.close();
            reader.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void normalizeSections(String str){
        String csvFile = str;
        String outFile = "/home/shamin/NetBeansProjects/CSVReader/Files/normalizedSections.csv";

        CSVReader reader = null;
        List<String[]> data = new ArrayList<String[]>();

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(outFile));

            reader = new CSVReader(new FileReader(csvFile));
            
            String[] line;
            while ((line = reader.readNext()) != null) {
                
                String gp = line[4];
                
                if(gp.startsWith("TBD")==true || gp.length()==0){
                    gp= "TBD";
                    
                }
            
                line[4]= gp;               
//                String add = line[0] + ", " + line[1] + ", " + line[2] + ", " + line[3] + ", " + line[4];
                writer.writeNext(line);
                
            }
            
            writer.close();
            reader.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void normalizeGrades(String str){
        String csvFile = str;
        String outFile = "/home/shamin/NetBeansProjects/CSVReader/Files/normalizedGrades.csv";

        CSVReader reader = null;
        List<String[]> data = new ArrayList<String[]>();

        try {
            CSVWriter writer = new CSVWriter(new FileWriter(outFile));

            reader = new CSVReader(new FileReader(csvFile));
            
            String[] line;
            while ((line = reader.readNext()) != null) {
                
                String gp = line[5];
                if(gp.contains(".")==false){
                    gp+= ".00";
                }
            
                line[5]= gp;               
//                String add = line[0] + ", " + line[1] + ", " + line[2] + ", " + line[3] + ", " + line[4] + ", " + line[5] + ", " + line[6];
                writer.writeNext(line);
                
            }
            
            writer.close();
            reader.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void readAndPrint(String str){
        String csvFile = str;

        CSVReader reader = null;
        try {
            reader = new CSVReader(new FileReader(csvFile));
            String[] line;
            while ((line = reader.readNext()) != null) {
//                System.out.println(line[0] + ", " + line[1] + " " + line[2] + ", " + line[3] + ", " + line[4] + ", " + line[5]);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
  
