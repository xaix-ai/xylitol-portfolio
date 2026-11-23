# Portfolio images

Put your pictures in these folders, then type the path in Django admin.

| Folder          | Used for                                   | Type this in the admin           |
|-----------------|--------------------------------------------|----------------------------------|
| `profile/`      | About → your photo                         | `profile/me.jpg`                 |
| `projects/`     | Projects → screenshots / screen recordings | `projects/sales-dashboard-1.png` |
| `certificates/` | Certificates → picture of the certificate  | `certificates/google-data.png`   |
| `achievements/` | Achievements → photo                       | `achievements/hackathon.jpg`     |

Tips

- File names: lowercase, no spaces (use `-`), e.g. `sales-dashboard-1.png`.
- Screenshots look best at 16:10 or 16:9 (e.g. 1440 × 900). Phone screenshots work too.
- Keep each image under ~500 KB. Compress at https://squoosh.app (WebP or JPG).
- Screen recordings: `.mp4` or `.webm`, short (5–15 s), no sound, under ~5 MB.
- After adding new files: commit and push them with GitHub Desktop, or they
  won't exist on the live site.
- Instead of a file name you can also paste a full `https://` image link or a
  Google Drive share link (shared as "Anyone with the link").
- Check everything with: `python manage.py portfolio_check`
