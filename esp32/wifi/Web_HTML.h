/*****************************************************************************
* | File      	:   Web_Html.c
* | Author      :   Waveshare team
* | Function    :	  send html string
* |	This version:   V1.0
* | Date        :   2019-08-26
* | Info        :
*----------------
******************************************************************************/
extern  WebServer server;
extern  IPAddress myIP;

void Web_SendHTML()
{
    server.send(200, "text/html",
                "<!DOCTYPE html>\r\n"
                "<html>\r\n"
                "<head>\r\n"
                "<meta charset=\"utf-8\" />\r\n"
                "<title>12.48inch e-paper</title>\r\n"
                "</head>\r\n"
                "<link rel=\"stylesheet\" href=\"index.css\" />\r\n"
				"<link rel='icon' href='data:;base64,='>\r\n"
                "<script type=\"text/javascript\" src=\"https://ajax.aspnetcdn.com/ajax/jquery/jquery-3.5.1.min.js\"></script>\r\n"
                "<!-- <script type=\"text/javascript\" src=\"jquery.js\"></script> -->\r\n"
                "<script type=\"text/javascript\" src=\"Web_SendJS_A.js\" ></script>\r\n"
                "<script type=\"text/javascript\" src=\"Web_SendJS_A.js\" ></script>\r\n"
                "<body>\r\n"
                "<div class=\"large\">\r\n"
                "	<div class=\"Menu\">\r\n"
                "		<div class=\"Item\">\r\n"
                "			<a class=\"ch-home\" href=\"http://www.waveshare.net/\">微雪电子</a>\r\n"
                "			<a class=\"en-home\" href=\"http://www.waveshare.com/\">waveshare</a>\r\n"
                "		</div>\r\n"
                "		<li class=\"Nav\">\r\n"
                "			<form class=\"firstDeviceIP\">\r\n"
                "				IP : <input class=\"firstDeviceIPinput\" type=\"text\" id=\"DeviceIP\" value = \"\r\n"
                                + String(myIP[0],DEC)+'.'+String(myIP[1],DEC)+'.'+String(myIP[2],DEC)+'.'+String(myIP[3],DEC)+"\"> </input>\r\n"
                "			</form>\r\n"
                "			<div class=\"firstNav 12in48_epd-js\">12.48inch e-paper</div>\r\n"
                "			<div class=\"firstNav 12in48b_epd-js\">12.48inch e-paper b</div>\r\n"
                "		</li>\r\n"
                "		<button class=\"uploadimage_button\">upload image</button>\r\n"
                "	</div>\r\n"
                "	<div class=\"SubMenu\">\r\n"
                "		<div class=\"DrawingDrop\">\r\n"
                "			<div class=\"DrawingNav DrawPoint-js\">Draw Point</div>\r\n"
                "			<div class=\"DrawingNav DrawLine-js\">Draw Line</div>\r\n"
                "			<div class=\"DrawingNav DrawRectangle-js\">Draw Rectangle</div>\r\n"
                "			<div class=\"DrawingNav DrawCircle-js\">Draw Circle</div>\r\n"
                "			<div class=\"DrawingNav DrawString-js\">Draw String</div>\r\n"
                "			<div class=\"DrawingNav ShowPic-js\">Show Picture</div>\r\n"
                "		</div>\r\n"
                "	</div>\r\n"
                "	<div class=\"maincontent\">\r\n"
                "		<div class=\"header epd\" style=\"display: none\">\r\n"
                "			<div class=\"epdname\"></div>\r\n"
                "			<div class=\"epdpixelandcolor\"></div>\r\n"
                "		</div>\r\n"
                "		<div class=\"page pagewidth\" style=\"display: none\">\r\n"
                "			<!-- OVER -->\r\n"
                "			<div class=\"DrawCanvas pagewidth\">\r\n"
                "				<div class=\"DrawCanvastext\">Drop image here...</div>\r\n"
                "			</div>\r\n"
                "		</div>		\r\n"
                "		<div class=\"footer\" style=\"display: none\">\r\n"
                "			<div class=\"footername\">waveshare|深圳市微雪电子有限公司</div>\r\n"
                "		</div>\r\n"
                "	</div>\r\n"
                "</div>\r\n"
                "</body>\r\n"
                "</html>"
               );
}
