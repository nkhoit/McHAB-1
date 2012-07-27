package mcgill.mchab.balloon;

import android.os.Bundle;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import ioio.lib.api.DigitalOutput;
import ioio.lib.api.Uart;
import ioio.lib.api.exception.ConnectionLostException;
import ioio.lib.util.BaseIOIOLooper;
import ioio.lib.util.IOIOLooper;
import ioio.lib.util.android.IOIOActivity;
import android.os.Environment;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ToggleButton;

import mcgill.mchab.balloon.SD_Card;

/**
 * This is the main activity of the HelloIOIO example application.
 * 
 * It displays a toggle button on the screen, which enables control of the
 * on-board LED. This example shows a very simple usage of the IOIO, by using
 * the {@link IOIOActivity} class. For a more advanced use case, see the
 * HelloIOIOPower example.
 */
public class MainActivity extends IOIOActivity {
	private ToggleButton button_;
	private CheckBox check1_;
	private CheckBox check2_;
	private CheckBox check3_;
	private EditText edit1_;
	/**
	 * Called when the activity is first created. Here we normally initialize
	 * our GUI.
	 */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		button_ = (ToggleButton) findViewById(R.id.toggleButton1);
		check1_ = (CheckBox) findViewById(R.id.checkBox1);
		check2_ = (CheckBox) findViewById(R.id.checkBox2);
		check3_ = (CheckBox) findViewById(R.id.checkBox3);
		edit1_ = (EditText) findViewById(R.id.editText1);
		
		check1_.setChecked(true);
	}
	
	/**
	 * This is the thread on which all the IOIO activity happens. It will be run
	 * every time the application is resumed and aborted when it is paused. The
	 * method setup() will be called right after a connection with the IOIO has
	 * been established (which might happen several times!). Then, loop() will
	 * be called repetitively until the IOIO gets disconnected.
	 */
	class Looper extends BaseIOIOLooper {
		/** The on-board LED. */
		private DigitalOutput led_;
		private Uart uart_;
		private InputStream in_;
		private GPS_Manager gpsManager;
		private SD_Card gps_sdWriter;
		private GUI_Manager guiManager;
		private String gps_data;
		
		/**
		 * Called every time a connection with IOIO has been established.
		 * Typically used to open pins.
		 * 
		 * @throws ConnectionLostException
		 *             When IOIO connection is lost.
		 * 
		 * @see ioio.lib.util.AbstractIOIOActivity.IOIOThread#setup()
		 */
		@Override
		protected void setup() throws ConnectionLostException {
		    check2_.setChecked(true);
			
		    //Initialize GPS via uart
			uart_ = ioio_.openUart(6, 7, 4800, Uart.Parity.NONE, Uart.StopBits.ONE);
			in_ = uart_.getInputStream();
			gpsManager = new GPS_Manager(in_);
			
			led_ = ioio_.openDigitalOutput(0, true);
		    gps_sdWriter = new SD_Card(Environment.getExternalStorageDirectory(), "GPS_DATA", "gps_data_1");
		    guiManager = new GUI_Manager();
		    
		}

		/**
		 * Called repetitively while the IOIO is connected.
		 * 
		 * @throws ConnectionLostException
		 *             When IOIO connection is lost.
		 * 
		 * @see ioio.lib.util.AbstractIOIOActivity.IOIOThread#loop()
		 */
		@Override
		public void loop() throws ConnectionLostException 
		{
			check3_.setChecked(true);
			
			//GPS
			gps_data = gpsManager.readLine();
			gps_sdWriter.generateNoteOnSD(gps_data);
			
			//LED
			led_.write(!button_.isChecked());
			
			
			//GUI
			//guiManager.setEditText(edit, text)
			runOnUiThread(new Runnable()
			{
				public void run()
				{
					edit1_.setText(gps_data);
				}
			});
			
			try
			{
				Thread.sleep(100);
			} catch(InterruptedException e)
			{
				
			}
			
		}
	}

	/**
	 * A method to create our IOIO thread.
	 * 
	 * @see ioio.lib.util.AbstractIOIOActivity#createIOIOThread()
	 */
	@Override
	protected IOIOLooper createIOIOLooper() {
		return new Looper();
	}  
}