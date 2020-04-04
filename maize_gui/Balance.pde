
class Balance {
  int x; 
  int y;
  int width_height;
  float clamp; // defines +/- extent of input ranges for balance reticle, -clamp to +clamp horiz and vert.
  Balance(int x, int y, int width_height, float clamp) {
    this.x = x;
    this.y = y;
    this.width_height = width_height;
    this.clamp = clamp;
  }

  void drawBalance(float h_offset, float v_offset) {
    fill(0);
    rect(x, y, width_height, width_height);
    float half_x = x + (0.5 * width_height);
    float half_y = y + (0.5 * width_height);
    strokeWeight(1);
    stroke(255);
    line(half_x, y, half_x, y + width_height);
    line(x, half_y, x + width_height, half_y);
    float _x = (h_offset / clamp) * (0.5 * width_height);
    float _y = (v_offset / clamp) * (0.5 * width_height);
    fill(255, 255, 0);
    noStroke();
    circle(_x + half_x, _y + half_y, 6);
  }
}
