package mcgill.mchab.balloon;

import ioio.lib.api.IOIO;
import ioio.lib.api.Uart;
import ioio.lib.api.exception.ConnectionLostException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class GPS_Manager 
{
	InputStream in;
	private InputStreamReader inReader;
	private BufferedReader buffReader;
	
	GPS_Manager(InputStream in_)
	{
		in = in_;
		inReader = new InputStreamReader(in);
		buffReader = new BufferedReader(inReader);
	}
	
	String readLine()
	{
		String str = new String();
		
		// TO DO: change the algorithm so that it doesnt block when gps is disconnected
		try 
		{
			if(in.available() > 0)	
			{
				str = buffReader.readLine();
				str += "\n";
			}
		} 
		catch (IOException e1)
		{
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		return str;
	}

}
