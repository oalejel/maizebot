
public class Maze {
  Boolean showTrace = true;
  int mazeWidth = 0;
  int ballX = 0; 
  int ballY = 0; 
  ArrayList<ArrayList<Integer>> mazeArr;

  public Maze() {
    mazeArr = new ArrayList<Integer>(100);
  }

  public void draw_map() {
    float scale_factor = min(self.maze_width / float(len(maze_map[0])), height / float(len(maze_map)));
    float x = 0;
    float y = 0;
    noStroke();
    for (int r_index = 0; r_index < maze_map.length(); r_index++) {
      x = 0;
      for (int c_index = 0; c_index < row[]; c_index++) {
        if (entry == 0) { // if floor, draw white at this pixel
          fill(255)
        } else if (entry == 1) { // wall 
          fill(255, 0, 0);
        } else { // hole, fill with gray 
          fill(0);
          x += scale_factor;
          rect(x, y, scale_factor, scale_factor);
        }  
        y += scale_factor
      }
    }
  } 


  void draw_controls() { 
    global maze_width 
      fill(32, 100, 40)
  }

  void update_map() {
  }

  void update_ball() {
  }

  void update_controls() {
  }        

  // fake map generation
  void make_fake_map() { 
    example_width = 400
      maze_map = Array<int>
      for y in range(0, 300):
    maze_map.append([0] * example_width) # add a new row 
      for x in range(0, example_width):
  if y < 10 or y > 290 or x < 10 or x > 390:
    maze_map[y][x] = 1
    else: 
    maze_map[y][x] = 0
  }
}
