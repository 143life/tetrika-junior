def strict(func):
	def wrapper(*args, **kwargs):
		# check args
		for (annotation, arg_type), num in zip(func.__annotations__.items(), args):
			if arg_type != type(num):
				raise TypeError("the type of value passed to the " \
					f"parameter \"{annotation}\" does not match the type " \
					"declared in the function prototype")
		# check kwargs
		for kwarg, value in kwargs.items():
			if kwarg in func.__annotations__:
				if func.__annotations__[kwarg] != type(value):
					raise TypeError("the type of value passed to the " \
					f"parameter \"{kwarg}\" does not match the type " \
					"declared in the function prototype")
		return func(*args, **kwargs)
	return wrapper

# test 1
@strict
def greet(a: bool, c: int, b: int, d: str):
	return 'Hello!'

def main():
	print(greet(True,2,3, d=""))
	return

main()