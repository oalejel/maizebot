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
    rect(this.x, this.y, this.width_height, this.width_height);
    float half_x = this.x + (0.5 * this.width_height);
    float half_y = this.y + (0.5 * this.width_height);
    strokeWeight(1);
    stroke(255);
    line(half_x, this.y, half_x, this.y + half_y);
    line(this.x, half_y, this.x + this.width_height, half_y);
    float _x = (h_offset / self.clamp) * (0.5 * self.width_height);
    float _y = (v_offset / self.clamp) * (0.5 * self.width_height);
    fill(255, 255, 0);
    circle(_x + half_x, y + half_y, 6);
  }
}
