
import processing.net.*;

Maze maze;
Balance balance;

Server s; 
Client c;
String input;
int data[];

void setup() {
  size(900, 500); // draw a 700 by 500 window
  maze = new Maze(width - 200, height);
  balance = new Balance(maze.frameWidth + 10, 10, 50, 10);


  text("Balance", maze.frameWidth + 10, 10);

  balance.drawBalance(0, 0);
  maze.makeFakeMap();
}

void draw() {
  maze.drawMap();
}

void keyPressed() {
  if (key == 't') {
    // to show trace
    maze.showTrace = !maze.showTrace;
  }
}
