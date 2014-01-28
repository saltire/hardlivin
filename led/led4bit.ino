#include <Adafruit_GFX.h>
#include <RGBmatrixPanel.h>

#define CLK 8  // MUST be on PORTB!
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

uint8_t x = 0, y = 0;

void setup() {
	matrix.begin();
	Serial.begin(9600);
}

void loop() {
	while (Serial.available() >= 3 && (x < 12 || y < 12)) {
		uint8_t byte1 = Serial.read();
		uint8_t byte2 = Serial.read();
		uint8_t byte3 = Serial.read();
		
		uint8_t r1 = byte1 / 16 << 4;
		uint8_t g1 = byte1 % 16 << 4;
		uint8_t b1 = byte2 / 16 << 4;
		matrix.drawPixel(x, y, matrix.Color888(r1, g1, b1, 1));
		
		uint8_t r2 = byte2 % 16 << 4;
		uint8_t g2 = byte3 / 16 << 4;
		uint8_t b2 = byte3 % 16 << 4;
		matrix.drawPixel(x + 1, y, matrix.Color888(r2, g2, b2, 1));
		
		byte coords[] = {byte(x), byte(y), byte(r1), byte(g1), byte(b1)};
		Serial.write(coords, 5);
		
		x += 2;
		if (x == 12) {
			x = 0;
			y += 1;
		}
	}
}
