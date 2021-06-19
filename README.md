## Requirements
* Python 3.8+
* Installation of requirements.txt `pip install -r requirements.txt`

## Usage
* Windows: `python deity.py file_path <'debug'>`
* Linux: `./deity.py file_path <'debug'>` or `python3 deity.py file_path <'debug'>`
* Run all tests: Replace file_path with `runall`

## Operators
* Less Than: `a < b`
* Greater Than: `a > b`
* Less than or equal to: `a <= b`
* Greater than or equal to: `a >= b`
* Equal: `a == b` or `a === b`
* Inequal: `a != b` or `a !== b`
* And: `a && b`
* Or: `a || b`
* Logical not: `!a`
* Addition: `a + b`
* Subtraction: `a - b`
* Multiplication: `a * b`
* Division: `a / b`
* Modulo: `a % b`
* Accessor: `a.b`
* Pipe: `(a) | (b)` where `a` is an expression(s), and `b` is a function

## Types
* obj (for unknown or flexible types)
* string
* int
* float
* null
* boolean

### Constants
* true
* false
* null

### Standard Library
* `put(args...)` -> Standard print function
* `urlreq.get(url)` -> GET request to specified url
* `memaddr(obj)` -> Retrieves memory address for obj
* `input(prompt[, callable])` -> Retrieves user input with an optional `callable` param to evaluate the validity of the result of user input, continues callable evaluates to true
* `converter.to_integer(x)` -> Attempts to convert `x` to an integer
* `converter.to_float(x)` -> Attempts to convert `x` to a float
* `converter.to_string(x)` -> Converts `x` to a string
* `converter.to_boolean(x)` -> Evaluates the truthiness of `x` and returns it

## Functions

##### Declaration
```rust
fn my_func(int param1, string param2) : return_type {
    // fn body
    return value;
}
```

##### Usage
```rust
my_func(123, "abc");
```

## Variables

##### Declaration
```rust
string my_string = "abc";
int my_int = 123;
boolean x = true;
boolean y = false;
```

##### Reassignment
```rust
my_string = "def";
my_int = 456;
```

## Control Flow

##### If statement
```rust
string a = "abc";

if (a == "abc") { // parentheses optional
    put("a is abc");
} else if (a == "def") {
    put("a is def");
}
```

##### For loop
```rust
for int i : (1, 10) { // (1, 10, 1) (start, stop[, step=1])
    put(i);
}
```

##### While loop
```rust
int i = 0;

while (i < 30) {
    put(i);
    i = i + 1;
}
```