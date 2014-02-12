#include <Adafruit_GFX.h>
#include <RGBmatrixPanel.h>

#define CLK 8  // MUST be on PORTB!
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);


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

void draw_title() {
	Serial.write('C');

	int16_t row[32];
	int8_t x = 0, y = 0;

	while (y < 16) {
		if (Serial.available() >= 3) {
			uint8_t byte1 = Serial.read();
			uint8_t byte2 = Serial.read();
			uint8_t byte3 = Serial.read();

			row[x] = matrix.Color888(
					byte1 / 16 << 4,
					byte1 % 16 << 4,
					byte2 / 16 << 4, 1);
			row[x + 1] = matrix.Color888(
					byte2 % 16 << 4,
					byte3 / 16 << 4,
					byte3 % 16 << 4, 1);

			Serial.write(1);
			x += 2;
			if (x == 32) {
				for (uint8_t xx = 0; xx < 32; xx++) {
					matrix.drawPixel(xx, y, row[xx]);
				}

				x = 0;
				y++;
			}
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

// this will scroll [count] squares across the screen
// there is a brief pause in the middle when we load the next image
void scroll_continuous(uint8_t count, uint8_t speed, uint8_t pause) {
	int16_t image1[12][12];
	int16_t image2[12][12];
	request_square(image2);
	int16_t col[12];

	// scroll image 2 onto the screen
	for (int8_t xoff = 9; xoff >= -12; xoff--) {
		matrix.fillScreen(0);
		draw_square(xoff + 22, 2, image2);
		delay(speed);
	}
	delay(pause);

	// swap image2 into image1, load a new image2
	// then scroll image1 off and image2 on simultaneously
	for (uint8_t i = 1; i < count; i++) {
		memcpy(image1, image2, sizeof(image2));
		request_square(image2);

		for (int8_t xoff = 9; xoff >= -12; xoff--) {
			matrix.fillScreen(0);
			draw_square(xoff, 2, image1);
			draw_square(xoff + 22, 2, image2);
			delay(speed);
		}
		delay(pause);
	}

	// scroll image1 off the screen
	for (int8_t xoff = 9; xoff >= -12; xoff--) {
		matrix.fillScreen(0);
		draw_square(xoff, 2, image2);
		delay(speed);
	}
}

void scroll_multiple(uint8_t repeat, uint8_t speed) {
	int16_t image1[12][12];
	int16_t image2[12][12];
	int16_t image3[12][12];
	//int16_t image4[12][12];
	request_square(image1);
	request_square(image2);
	request_square(image3);

	//int16_t col[12];

	for (int8_t xoff = 2; xoff >= -24; xoff--) {
//		if (xoff < -10 && xoff >= -22) {
//			request_column(col);
//			for (uint8_t y = 0; y < 12; y++) {
//				image4[-10 - xoff][y] = col[y];
//			}
//		}

		matrix.fillScreen(0);
		draw_square(xoff, 2, image1);
		draw_square(xoff + 14, 2, image2);
		draw_square(xoff + 28, 2, image3);
		//draw_square(xoff + 42, 2, image4);

		delay(speed);
	}
}

void setup() {
	matrix.begin();
	Serial.begin(9600);
}

void loop() {
	draw_title();
	delay(3000);

	scroll_continuous(10, 100, 1000);
}
