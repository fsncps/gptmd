## GPTMD
Intercepts the conversation json for a ChatGPT URL and converts the thread to markdown.

Clone to ~/.local/share, move file and make it executable:
```bash
git clone github.com/fsncps/gptmd.git ~/.local/share
mv ~/.local/share/gptmd ~/.local/bin/
chmod +x ~/.local/bin/gptmd
```
Then use with URL and threadname to save threadname.json and threadname.md, e.g.
```bash
gptmd https://chatgpt.com/g/g-p-67ef5dxxxx interesting_convo
```

Authorization token is automatically extracted for Librewolf, other browsers TBD. Disable calling `update_token()` in main and copy manually from browser tools, combine values of __Secure-next-auth.session-token.0 and __Secure-next-auth.session-token.1 in token.txt.

