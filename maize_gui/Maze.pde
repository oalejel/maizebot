
public class Maze {
  Boolean showTrace = true;
  int frameWidth = 0; // the width we draw the maze width on screen. not necessarily same as array dimensions
  int frameHeight = 0;
  int ballX = 0; 
  int ballY = 0; 
  ArrayList<ArrayList<Integer>> mazeArr;

  public Maze(int w, int h) {
    this.frameWidth = w; 
    this.frameHeight = h;
  }

  public void drawMap() {
    int numCols = mazeArr.get(0).size();
    int numRows = mazeArr.size();
    float scaleFactor = min(frameWidth / (float)numCols, frameHeight / (float)numRows);

    // loop params used to draw 
    float x = 0;
    float y = 0;

    // reset drawing context 
    noStroke();

    for (int row = 0; row < numRows; row++) {
      for (int col = 0; col < numCols; col++) {
        int entry = mazeArr.get(row).get(col);
        if (entry == 0) { // if floor, draw white at this pixel
          fill(255);
        } else if (entry == 1) { // wall 
          fill(255, 0, 0);
        } else { // hole, fill with gray 
          fill(0);
        }  
        rect(x, y, scaleFactor, scaleFactor);
        x += scaleFactor;
      }
      // prepare for next row
      x = 0;
      y += scaleFactor;
    }
  } 


  void draw_controls() { 
    fill(32, 100, 40);
  }

  void update_map() {
  }

  void update_ball() {
  }

  void update_controls() {
  }        

  // fake map generation
  void makeFakeMap() { 
    int example_width = 400;
    int example_height = 300;
    mazeArr = new ArrayList<ArrayList<Integer>>(example_height);
    
    for (int y = 0; y < example_height; y++) {
      mazeArr.add(new ArrayList<Integer>());
      println(y);
      println(mazeArr.size());
      for (int x = 0; x < example_width; x++) {
        mazeArr.get(y).add(0);
        if (y < 10 || y > 290 || x < 10 || x > 390) {
          mazeArr.get(y).set(x, 1); // wall on boundaries
        }
      }
    }
  }
}
