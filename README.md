My configuration files, plugins etc. for [Sublime Text 2](https://sublimetext.com/2).

## Notes

### Platform-specific settings

It seems platform-specific settings in the User package folder are not possible at the moment.
`User/Preferences (OSX).sublime-settings` etc. would have been nice but doesn't work.
Therefore, I put my font settings in the Default folder:

`Default/Preferences (OSX).sublime-settings`:
```json
"font_face": "Inconsolata",
"font_size": 15.0,
"small_font_size": 15.0,
"large_font_size": 22.0,
```

`Default/Preferences (Windows).sublime-settings`:
```json
"font_face": "Consolas",
"font_size": 11
```

### Linux

No configuration for Linux here, only Windows and OSX.
