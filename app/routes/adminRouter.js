import express from 'express';
import basicAuth from 'express-basic-auth';
import { renderAdminPage } from '../controllers/adminController.js';
import { updateExperimentConfig } from '../configuration/experimentConfig.js';

const router = express.Router();

router.use(
  basicAuth({
    users: { [process.env.ADMIN_USER]: process.env.ADMIN_PASSWORD },
    challenge: true,
    realm: 'AdminArea',
    unauthorizedResponse: (req) => {
      const hadAuthHeader = Boolean(req.headers.authorization);
      const referer = req.get('Referer') || '/';
      const message = hadAuthHeader
        ? 'Wrong Username or Password.'
        : 'Authentication required. If Auth-Popup is not showing, try reloading the page.';

      return `<!doctype html>

<html lang="de">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Access blocked</title>
  <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate" />
  <style>
    body{font-family:system-ui,Arial,sans-serif;background:#f7f7f8;color:#111;padding:28px}
    .card{max-width:760px;margin:48px auto;padding:20px;border-radius:10px;background:#fff;box-shadow:0 6px 18px rgba(0,0,0,0.06)}
    h1{margin:0 0 8px;font-size:20px}
    p{margin:0 0 16px}
    .actions{margin-top:12px}
    button{padding:8px 12px;border-radius:6px;border:1px solid #ccc;background:#efefef;cursor:pointer}
    a{margin-left:12px}
    small{display:block;margin-top:12px;color:#666}
  </style>
</head>
<body>
  <div class="card" role="main" aria-live="polite">
    <h1>Access blocked</h1>
    <p>${message}</p>

    <div class="actions">
      <button id="btn-cancel" type="button">Cancel</button>
    </div>
  </div>

  <script>
    (function () {
      const referer = ${JSON.stringify(referer)};
      document.getElementById('btn-cancel').addEventListener('click', function () {
        window.location.href = '/';
      });
      setTimeout(function () {
        try {
          if (document.referrer) {
            history.back();
          } else {
            window.location.href = '/';
          }
        } catch (e) {
          // no-op
        }
      }, 3000);
    })();
  </script>
</body>
</html>`;
    },
  }),
);


router.post('/experiment-groups', async (req, res) => {
  const selected = req.body.groups; // string | array | undefined
  const useAll = req.body.useAll === 'on';

  const enabled = [];
  if (Array.isArray(selected)) enabled.push(...selected);
  else if (typeof selected === 'string') enabled.push(selected);

  // speichere in Mongo (await)
  await updateExperimentConfig({ enabledGroups: enabled, useAllGroups: useAll });

  const redirectTarget = req.baseUrl && req.baseUrl !== '' ? req.baseUrl : '/admin';
  return res.redirect(303, redirectTarget);
});

router.get('/', renderAdminPage);

export default router;
