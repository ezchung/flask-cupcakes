"use strict";

class Cupcake {
  /** Make instance of Cupcake from data object about cupcake:
   *   - {flavor, size, rating, image}
   */
  constructor({ flavor, size, rating, image }) {
    this.flavor = flavor;
    this.size = size;
    this.rating = rating;
    this.image = image;
  }

  /** Parsing cupcake from cupcakeID */
  static getCupcakeID(cupcake) {
    return cupcake.id;
  }
}

class CupcakeList {
  /** Generates a new CupcakeList
   *
   */
}

//given data about cupcake, generate html

//Get initial cupcakes. Return [{cupcake},....]

// Put initial cupcakes on page

// handle form for adding new cupcakes

// handle clicking delete: delete cupcake
