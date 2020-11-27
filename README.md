# **A Star Algorithm Visualization**
This is a program implemented to learn more about A* algorithm.

## Features
  * Choose one of four heuristics below  
    |Manhattan|Chebyshev|Octile|Euclidean|
    |:-------:|:-------:|:----:|:-------:|
    |<img src="https://user-images.githubusercontent.com/48203569/100442237-0688ab80-30eb-11eb-8159-ddaddccaab13.png" height="120" width="250">|<img src="https://user-images.githubusercontent.com/48203569/100442242-07214200-30eb-11eb-8490-97e1d073b24e.png" height="120" width="250">|<img src="https://user-images.githubusercontent.com/48203569/100442249-07b9d880-30eb-11eb-9e47-f317d065d9a7.png" height="120" width="250">|<img src="https://user-images.githubusercontent.com/48203569/100442244-07214200-30eb-11eb-81b2-160d02ef6484.png" height="120" width="250">|
  * Control weight
  * Drag to create/remove a wall
  * Choose between heap queue and list for open/closed list data structure
  * Allow diagonal movement

## Usage
  ```  
  // if pygame is not installed
  pip install pygame
  
  // visual_astar.py and PrStart.ttf(Font) files must be in the same path
  python3 visual_astar.py
  ```
  
  * Color  
    * Red : start point
    * Green : end point
    * Yellow : points in open list
    * Orange : points in closed list
    * Grey : Path
    * Black : Wall

## Demo
  <img src="https://user-images.githubusercontent.com/48203569/100443725-94659600-30ed-11eb-996a-effe05e8c2f1.gif" height="500" width="500">

## Library used
  * [pygame](https://www.pygame.org/news)
