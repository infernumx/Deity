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

## Functions

##### Declaration
```go
fn my_func(int param1, string param2) : return_type {
    // fn body
}
```

##### Usage
```go
my_func(123, 'abc');
```

## Variables

##### Declaration
```go
string my_string = 'abc';
string my_string = "abc";
int my_int = 123;
```

##### Reassignment
```go
my_string = 'def';
my_string = "def";
my_int = 456;
```

## Control Flow

##### If statement
```go
string a = 'abc';

if (a == 'abc') { // parentheses optional
    put('a is abc');
}
```