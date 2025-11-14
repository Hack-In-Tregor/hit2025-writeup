# reverse : Dinoojail
**Challenge Author(s)**: tabarnhack
**Difficulty**: Moyen

## Synopsis

Cette jail Python semble cacher quelque chose !

## Steps to solve 

De nombreuses commandes semblent restreindre l'usage de la jail Python. On obtient en effet beaucoup de
```python
❌ Unauthorized code!
```

Cependant, après quelques recherches, la commande `print(globals())` permettant d'afficher les variables globales nous renvoie un résultat très intéressant.

```python
>>> print(globals())
{'__builtins__': {'len': <built-in function len>, 'str': <class 'str'>, 'int': <class 'int'>, 'list': <class 'list'>, 'dict': <class 'dict'>, 'tuple': <class 'tuple'>, 'set': <class 'set'>, 'bool': <class 'bool'>, 'abs': <built-in function abs>, 'min': <built-in function min>, 'max': <built-in function max>, 'sum': <built-in function sum>, 'print': <built-in function print>, 'range': <class 'range'>, 'enumerate': <class 'enumerate'>, 'zip': <class 'zip'>, 'map': <class 'map'>, 'filter': <class 'filter'>, 'sorted': <built-in function sorted>, 'reversed': <class 'reversed'>, 'dir': <built-in function dir>, 'globals': <built-in function globals>}, '__name__': '__main__', 'dis': <module 'dis' from '/usr/lib/python3.12/dis.py'>, 'restricted_shell': <function restricted_shell at 0x750799ea5580>, 'shell': <function shell at 0x750799d73880>, 'is_safe': <function is_safe at 0x750799fda2a0>, 'BLACKLIST': frozenset({'getattr', 'subprocess', 'copyright', 'delattr', '__builtins__', 'setattr', 'quit', '__import__', 'exec', 'locals', 'import', 'os', 'exit', 'vars', 'credits', 'hasattr', 'callable', 'breakpoint', 'raw_input', 'input', 'compile', 'help', 'eval', 'license', 'reload', 'file', 'builtins', 'sys', 'open'})}
```

On constate plusieurs choses. Tout d'abord une fonction shell semble être présente, mais cette dernière demande un mot de passe.

```python
>>> shell()
🙈 Password:
⛔️ No way you are an admin
```

Mais ce qui est encore plus intéressant c'est la présence du module `dis`, ce qui permet de désassembler le bytecode Python. Ainsi on peut retrouver le mot de passe permettant d'executer la commande shell

```python
>>> dis.dis(shell)
119           0 RESUME                   0

120           2 LOAD_GLOBAL              1 (NULL + input)
             12 LOAD_CONST               1 ('🙈 Password: ')
             14 CALL                     1
             22 LOAD_ATTR                3 (NULL|self + strip)
             42 CALL                     0
             50 LOAD_CONST               2 ('abc123')
             52 COMPARE_OP              40 (==)
             56 POP_JUMP_IF_FALSE       42 (to 142)

121          58 LOAD_GLOBAL              5 (NULL + print)
             68 LOAD_CONST               3 ('Welcome to heaven my lord! 🙏')
             70 CALL                     1
             78 POP_TOP
             ...
```

Le mot de passe du shell est `abc123`. Ainsi on peut récupérer le flag final se trouvant dans le même répertoire.

```python
>>> shell()
🙈 Password: abc123
Welcome to heaven my lord! 🙏
>>> os.listdir()
['Dockerfile', 'flag.txt', 'dinoojail.py']
>>> open('flag.txt').read()
hit{Is_it_ajail_or_a_rev_chall}
```