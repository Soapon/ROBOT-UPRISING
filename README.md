# ROBOT-UPRISING
Rules:
1. Player starts w/ 3 hearts
2. Press Space to shoot
3. WASD or Arrow keys to move
4. Powerup by using the "E" Key
5. When the robot hit the player or reach the right side, the player lose a heart

## What went well
One thing that went better than I expected was coordinating timing in the game. There were a lot of timing parameters, such as enemy spawning and the duration of animations, that required keeping multiple variables flowing naturally. Those systems ultimately worked together smoothly. I was especially proud of how the jump and power-up mechanic functioned, which was highly requested, including the temporary freeze at the top and the destruction of enemies.

## What didn't go well
As the code grew bigger, debugging became harder. The BIGGEST error I ran into that I had trouble with was a bug where the player sprite simply would not appear. To debug this error, I rebuilt the entire code and matched my code to the tutorial line by line to see exactly why the error is happening. (Problem that I ran into and fix): Additionally, for my enemy tracking, I tried to rely only on sprite lists as I did for the player, but that made it difficult to track enemy data. If I had only the arcade SpriteList, I'd lose access to the Enemy object's animation state and update methods.

## What I can do better next time
Next time, I would balance my focus on pure code with earlier consideration of visuals because I went into the coding with the coding architecture in mind but I didn't think about how to transfer that onto the player interface. I spent a lot of time making systems logically sound, which led to issues with spacing and movement once the game was rendered. Prototyping visuals earlier with placeholder assets would help reveal these problems sooner. If I had more time, I want to make the game progressively faster as the game goes on as well as giving the drones different health values. I also want to make the animation effect for the special ability cooler by adding a laser that runs through entire screen..

## User feedback
Users wanted more diverse enemies spawning/movement mechanics, which I would be open to adding if given more time. Additionally, users wanted rounds of enemies instead of constant spawning. Users also want a different explosion effect when the user collides with the enemy drone to make it clear that the user lost health or have a separate effect that indicates that the user has lost health.
## Course feedback
I think it would be a lot better if we were able to figure out the download/compilation error for the packages we used beforehand (I wanted to use pygame T-T). Another thing I think would be helpful is to have a smaller assignment before the final just to get us familiar with the new package.