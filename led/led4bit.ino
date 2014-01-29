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

void request_column(int16_t col[]) {
	Serial.write('B');

	uint8_t y = 0;
	while (y < 12) {
		if (Serial.available() >= 3) {
			uint8_t byte1 = Serial.read();
			uint8_t byte2 = Serial.read();
			uint8_t byte3 = Serial.read();

			col[y] = matrix.Color888(
					byte1 / 16 << 4,
					byte1 % 16 << 4,
					byte2 / 16 << 4, 1);
			col[y + 1] = matrix.Color888(
					byte2 % 16 << 4,
					byte3 / 16 << 4,
					byte3 % 16 << 4, 1);
			y += 2;
		}
	}
}

void request_square(int16_t image[12][12]) {
	int16_t col[12];
	for (uint8_t x = 0; x < 12; x++) {
		request_column(col);
		for (uint8_t y = 0; y < 12; y++) {
			image[x][y] = col[y];
		}
	}
}

void draw_square(int8_t xoff, int8_t yoff, int16_t image[12][12]) {
	for (uint8_t y = 0; y < 12; y++) {
		for (uint8_t x = 0; x < 12; x++) {
			matrix.drawPixel(x + xoff, y + yoff, image[x][y]);
		}
	}
}

void scroll_left(uint8_t repeat, uint8_t speed) {
	int16_t image[12][12];
	request_square(image);

	for (uint8_t i = 0; i < repeat; i++) {
		for (int8_t xoff = 32; xoff >= -12; xoff--) {
			matrix.fillScreen(0);
			draw_square(xoff, 2, image);
			delay(speed);
		}
	}
}

void scroll_multiple(uint8_t repeat, uint8_t speed) {
	//int16_t image1[12][12];
	int16_t image2[12][12];
	int16_t image3[12][12];
	int16_t image4[12][12] = {0};
	//request_square(image1);
	request_square(image2);
	request_square(image3);

	int16_t col[12];

	for (int8_t xoff = 2; xoff >= -24; xoff--) {
		matrix.fillScreen(0);
		//draw_square(xoff, 2, image1);
		draw_square(xoff + 14, 2, image2);
		draw_square(xoff + 28, 2, image3);

		if (xoff < -10) {
			request_column(col);
			for (uint8_t y = 0; y < 12; y++) {
				image4[xoff + 10][y] = col[y];
			}
			draw_square(xoff + 42, 2, image4);
		}

		delay(speed);
	}
}

void loop() {
	scroll_left(1, 100);
	//scroll_multiple(1, 100);
}
