# SublimeText Indent plugin

What is the goal of Indent plugin? Short answer is converting this XML

```xml
<root><node attr="1" attr2="4"><node /></node></root>
```

to this:

```xml
<root>
    <node attr="1" attr2="4">
        <node/>
    </node>
</root>
```

Looks good? It also can convert this JSON

```json
{ "root": [ { "field": "val1", "field2": "val2" }, { "arr": [1, 3, "three"] }] }
```

to this

```json
{
    "root": [
        {
            "field": "val1",
            "field2": "val2"
        },
        {
            "arr": [
                1,
                3,
                "three"
            ]
        }
    ]
}
```

Want more? It can indent only selected text - including multiple selections and even mixed XML / JSON selections. It is smart enough to recognize XML or JSON even if you are editing plain text. Indent plugin won't mess up your keyboard shortcuts because it uses "chord" command Ctrl+K, Ctrl+F (this means hold Ctrl, press K then press F, release Ctrl) and also available in "Selection" menu.

## Supported Sublime Text versions
Indent plugin supports both Sublime Text 2 and Sublime Text 3

## Installation
Just use [Package Control](https://packagecontrol.io/) and search for "indent xml" plugin.

## Usage
Click on Tools->Command Pallette... (or Ctrl+Shift+P if you're a keyboard guy) and then chose "Indent XML".

## Settings
Preferences -> Package Settings -> Indent XML

## Feedback & Support
Available on [Github](https://github.com/alek-sys/sublimetext_indentxml)

## Contribution
...is always welcome! Same place - [Github](https://github.com/alek-sys/sublimetext_indentxml)

## License
This software is distributed under MIT license (see License.txt for details).
