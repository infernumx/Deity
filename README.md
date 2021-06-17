## Requirements
* Python 3.8+
* Installation of requirements.txt `pip install -r requirements.txt`

## Usage
* Windows: `python deity.py file_path <'debug'>`
* Linux: `./deity.py file_path <'debug'>` or `python3 deity.py file_path <'debug'>`

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
* Accessor: `a.b`
* Pipe: `(a) | (b)` where `a` is an expression(s), and b is a function

## Types
* obj (for unknown or flexible types)
* string
* int
* float
* null

### Constants
* true
* false
* null

### Standard Library
* `put(args...)` -> Standard print function
* `urlreq.get(url)` -> GET request to specified url
* `memaddr(obj)` -> Retrieves memory address for obj

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
my_func(123, 'abc');
```

## Variables

##### Declaration
```rust
string my_string = 'abc';
string my_string = "abc";
int my_int = 123;
```

##### Reassignment
```rust
my_string = 'def';
my_string = "def";
my_int = 456;
```

## Control Flow

##### If statement
```rust
string a = 'abc';

if (a == 'abc') { // parentheses optional
    put('a is abc');
}
```