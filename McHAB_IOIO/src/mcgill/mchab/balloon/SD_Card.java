package mcgill.mchab.balloon;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class SD_Card 
{
	private File gpxfile;
	private FileWriter gps_writer;
	
	SD_Card(File storageDirectory, String rootName, String fileName)
	{
	    File root = new File(storageDirectory, rootName);      
		
		//Make root directory if it does not exist
	    if (!root.exists()) 
	    {
	        root.mkdirs();
	    }
		
		try 
		{
			gpxfile = new File(root, fileName);
			gps_writer = new FileWriter(gpxfile);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void generateNoteOnSD(final String sBody) 
	{
	   try
	   {
		   gps_writer.append(sBody);
           gps_writer.flush();
	   	} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
