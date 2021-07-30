<p style="text-align: justify;"><span style="text-decoration: underline;">Instructions for the FlightPi LCD Script by Matt Dyson (edited by Banham)</span></p>
<p style="text-align: justify;"><strong>This method only uses the LCD and does not utilise the NeoPixels or Arduino</strong></p>
<p style="text-align: justify;"><span style="text-decoration: underline;">Prerequisites</span></p>
<ul>
<li>Raspberry Pi 2B or better (I got mine from CEX for &pound;15)</li>
<li>Female-Female Dupont Cables (<a href="https://amzn.to/3k0B9dA" target="_blank" rel="noopener"><span style="color: #0563c1;">https://amzn.to/3k0B9dA</span></a>)</li>
<li>RTL2832U + R820T2 RTL-SDR ADS-B Antenna &amp; USB Receiver</li>
<li>20x04 LCD Module (<a href="https://www.aliexpress.com/item/1005002234319914.html" target="_blank" rel="noopener"><span style="color: #0563c1;">https://www.aliexpress.com/item/1005002234319914.html</span></a>) *</li>
<li>8GB Micro SD Card</li>
<li>Raspberry Pi WiFi Adapter (If your Pi does not have on-board WIFI)</li>
<li>Micro USB Cable &amp; Plug</li>
</ul>
<p style="text-align: justify;"><span style="text-decoration: underline;">Optional Prerequisites</span></p>
<ul>
<li>20x04 LCD Module Case (<a href="https://www.aliexpress.com/item/33040735359.html" target="_blank" rel="noopener">https://www.aliexpress.com/item/33040735359.html</a>) *</li>
<li>Raspberry Pi Case (<a href="https://bit.ly/39P5E1B" target="_blank" rel="noopener"><span style="color: #0563c1;">https://bit.ly/39P5E1B</span></a>) *</li>
<li>2M Micro USB Cable</li>
</ul>
<p style="text-align: justify;"><em>** Items Marked with an asterisk are purchased from AliExpress. For the best shipping time, I personally recommend using AliExpress Standard Shipping / ePacket / Cainiao Super Economy for Special Goods (UK only) as it can be quite slow otherwise.</em></p>
<p style="text-align: justify;"><span style="text-decoration: underline;">Installing Raspbian</span></p>
<p style="text-align: justify;">For this installation, I used Raspbian Buster, which will be handy later on. In order to install Raspbian Buster, head to <a href="https://www.raspberrypi.org/downloads/" target="_blank" rel="noopener"><span style="color: #0563c1;">https://www.raspberrypi.org/downloads/</span></a> and use either the Raspbian Image or the Raspbian Downloader.&nbsp;</p>
<p style="text-align: justify;">With the image, use Etcher in order to put this onto your MicroSD Card, which should be inserted into the PC. You should then proceed to flash the image which will be in your Downloads folder. Further instructions are available on the Etcher website.</p>
<p style="text-align: justify;">If you are using the installer, there is on screen instructions in order to assist you with the flashing. Simply check Raspberry Pi Buster Desktop (32-bit) and then insert your SD Card, let your PC detect it and then click Flash. There will be a notification pop-up when this has been completed.</p>
<p style="text-align: justify;">Once finished, take your MicroSD Card out and put it into your Raspberry Pi.</p>
<p style="text-align: justify;"><span style="text-decoration: underline;">Wiring Up</span></p>
<p style="text-align: justify;">Using your Dupont Cables, there will be 4 pins on the LCD Module i2c Backpack. They will be: GND, VCC, SDA, SCL. Wire as follows using any Dupont Cable:</p>
<div>
<table>
<tbody>
<tr>
<td><strong>LCD MODULE</strong></td>
<td><strong>RASPBERRY PI</strong></td>
</tr>
<tr>
<td>GND</td>
<td>PIN 6</td>
</tr>
<tr>
<td>VCC</td>
<td>PIN 2</td>
</tr>
<tr>
<td>SDA</td>
<td>PIN 3</td>
</tr>
<tr>
<td>SCL</td>
<td>PIN 5</td>
</tr>
</tbody>
</table>
</div>
<p style="text-align: justify;">Next, you should plug in your USB Devices, which will be the SDR USB (with Antenna plugged into the socket at the rear of the USB), along with your WiFi Adapter, should WiFi not be built into the Pi.</p>
<p style="text-align: justify;">Power up the Pi using the Micro USB Cable and any plug (I am using a standard Apple iPhone Plug)</p>
<p style="text-align: justify;"><span style="text-decoration: underline;">First Time Boot</span></p>
<p style="text-align: justify;">You will see the Pi is now in the primary set-up process, which will involve resizing the file system and running a few automatic commands. Wait for this to finish and the Pi should boot to the Desktop.</p>
<p style="text-align: justify;">Follow the on-screen instructions to finish Pi Setup, you may be asked to reboot.</p>
<p style="text-align: justify;"><span style="text-decoration: underline;">Enabling SSH and I2C</span></p>
<p style="text-align: justify;">Once rebooted, you should open the command line and run the following commands:</p>
<p style="text-align: justify;"><em>sudo apt-get update</em></p>
<p style="text-align: justify;"><em>sudo raspi-config</em></p>
<p style="text-align: justify;">When in raspberry pi config, you should open &lsquo;Advanced Options&rsquo; and then enable SSH and I2C. Once the operations have completed, close the configuration screen and save. If you don&rsquo;t know your Raspberry Pi&rsquo;s IP Address, you should then run this command:</p>
<p style="text-align: justify;"><em>hostname -I</em></p>
<p style="text-align: justify;">Remember to note this down, as we will need it next!</p>
<p style="text-align: justify;"><span style="text-decoration: underline;">Using SSH to install the software</span></p>
<p style="text-align: justify;">This step requires using the PuTTY Client, which can be downloaded here: <a href="https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html" target="_blank" rel="noopener"><span style="color: #0563c1;">https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html</span></a> . The PuTTY Client allows us to use SSH.</p>
<p>This screen will show up. Type in the Raspberry Pi IP Address which you might have noted down. It usually starts with 192.168.1.xx. The port should always be 22.</p>
<p>If there are any warnings, just press &lsquo;Yes&rsquo; and proceed. You will then be asked for credentials. The credentials will be:</p>
<p>Username: <em>pi</em></p>
<p>Password:<em> raspberry</em></p>
<p>Note, we are using the default credentials, so your Password may be different if you changed it in the set-up process.</p>
<p>We will be using dump1090-fa and PiAware, in order to install this, head to this webpage in order to find out more: <a href="https://flightaware.com/adsb/piaware/install" target="_blank" rel="noopener"><span style="color: #0563c1;">https://flightaware.com/adsb/piaware/install</span></a>.</p>
<p>If you wish, you can install as many feeders as you wish, you can also install FlightRadar24 Feeder, located here: <a href="https://bit.ly/2DuWzPg" target="_blank" rel="noopener"><span style="color: #0563c1;">https://bit.ly/2DuWzPg</span></a></p>
<p><span style="text-decoration: underline;">Installing the LCD Module Software &amp; Final Scripts</span></p>
<p>The LCD Module is connected over I2C, and we need to find its I2C Address, you can run this command here in order to find your address:</p>
<p><em>sudo i2cdetect -y 1</em></p>
<p>If the command is invalid, you probably don&rsquo;t have i2ctools installed, you can install this using:</p>
<p><em>sudo apt get install i2ctools</em></p>
<p>The i2c address will now be displayed, mine is 27, and the full address will be 0x27.</p>
<p>Let&rsquo;s install the script now. My repository has the updated API Links in order to make sure that it functions correctly. On the command line, run these commands:</p>
<p><em>git clone </em><a href="https://github.com/GalaxyTheoryz/flightpi.git" target="_blank" rel="noopener"><span style="color: #0563c1;"><em>https://github.com/GalaxyTheoryz/flightpi.git</em></span></a></p>
<p><em>cd flightpi</em></p>
<p><em>sudo nano FlightPi.py</em></p>
<p>You will now have entered the text editor for FlightPi.py, using the arrow keys, scroll down to&nbsp;</p>
<p><em>self.lcdThread = LcdThread(0x27,20)</em></p>
<p>You should replace &lsquo;27&rsquo; with your i2c address.</p>
<p>Next, head to this line:</p>
<p><em>self.sbsThread = SbsThread("mercury",30003)</em></p>
<p>You should replace &lsquo;mercury&rsquo; with your local IP address, it will look like 192.168.1.xx</p>
<p>We&rsquo;re now all done here, so save the file by doing CTRL+X and then press Y and then CTRL+X again.</p>
<p><span style="text-decoration: underline;">Final Steps</span></p>
<p>Almost there, but we need to install some Python Libraries first, run the following commands:</p>
<p><em>pip install threading2</em></p>
<p><em>pip install smbus</em></p>
<p>Now we&rsquo;re ready to boot up the python script, in order to do this, assuming you are in the flightpi directory, run this command:</p>
<p><em>python FlightPi.py</em></p>
<p>The LCD, within a few seconds will have now displayed a flight, being picked up by your antenna in the local area!</p>
<p>If this is not the case, please check your i2c address and your IP address in FlightPi.py</p>
