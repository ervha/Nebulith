# -*- coding: utf-8 -*-
with open('web/incremental.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''      if (!quoteMatch && depth === 0) {
        let indirect = cleanSource.match(/^(?:(.+?)[はが])?(.+?)と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
        if (!indirect) {
          indirect = cleanSource.match(/^(.+?)と(?:(.+?)[はが])?(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
          if (indirect) {
            indirect = [indirect[0], indirect[2], indirect[1], indirect[3]];
          }
        }
        if (indirect && !indirect[2].includes('こと')) {
          quoteMatch = indirect;
        }
      }'''

replacement = '''      if (!quoteMatch && depth === 0) {
        let indirect = cleanSource.match(/^(.+?)[は](.+?)と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
        if (!indirect) {
          indirect = cleanSource.match(/^(.+?)と(.+?)[はが](言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
          if (indirect) {
            indirect = [indirect[0], indirect[2], indirect[1], indirect[3]];
          }
        }
        if (!indirect) {
          const whole = cleanSource.match(/^(.+?)と(言った|言いました|言う|言います|思った|思いました|思う|思います)[。.]?$/);
          if (whole && !whole[1].includes('こと')) {
            indirect = [whole[0], null, whole[1], whole[2]];
          }
        }
        if (indirect && !indirect[2].includes('こと')) {
          quoteMatch = indirect;
        }
      }'''

if target in code:
    code = code.replace(target, replacement)
    with open('web/incremental.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print('SUCCESS: Updated indirect quote precision!')
else:
    print('Target not matched!')
