#include <Adafruit_GFX.h>
#include <RGBmatrixPanel.h>

#define CLK 8  // MUST be on PORTB!
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

void setup() {
	matrix.begin();
	Serial.begin(9600);
}

void request_square(int16_t image[12][12]) {
	Serial.write('A');

	uint8_t x = 0, y = 0;

	while (y < 12) {
		if (Serial.available() >= 3) {
			uint8_t byte1 = Serial.read();
			uint8_t byte2 = Serial.read();
			uint8_t byte3 = Serial.read();

			image[x][y] = matrix.Color888(
					byte1 / 16 << 4,
					byte1 % 16 << 4,
					byte2 / 16 << 4, 1);
			image[x + 1][y] = matrix.Color888(
					byte2 % 16 << 4,
					byte3 / 16 << 4,
					byte3 % 16 << 4, 1);

			Serial.write(1);

			x += 2;
			if (x == 12) {
				x = 0;
				y += 1;
			}
		}
	}
}

void scroll_left(uint8_t repeat, uint8_t speed) {
	int16_t image[12][12];
	request_square(image);

	int8_t yoff = 2;
	for (uint8_t i = 0; i < repeat; i++) {
		for (int8_t xoff = 32; xoff >= -12; xoff--) {
			matrix.fillScreen(0);
			for (uint8_t y = 0; y < 12; y++) {
				for (uint8_t x = 0; x < 12; x++) {
					matrix.drawPixel(x + xoff, y + yoff, image[x][y]);
				}
			}
			delay(speed);
		}
	}
}

void loop() {
	scroll_left(1, 100);
}
