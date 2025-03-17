import { Helmet } from 'react-helmet-async';

import { Box } from '@mui/material';

import { CONFIG } from 'src/config-global';

import Sidebar from 'src/sections/accountdetails/Sidebar';
import SamlSsoConfigPage from 'src/sections/accountdetails/account-settings/auth/components/saml-sso-config';

// ----------------------------------------------------------------------

const metadata = { title: `Authentication Settings  - ${CONFIG.appName}` };

export default function Page() {
  return (
    <>
      <Helmet>
        <title> {metadata.title}</title>
      </Helmet>
      <Box sx={{ display: 'flex', flexGrow: 1, overflow: 'hidden', zIndex: 0 }}>
        <Sidebar />
        <SamlSsoConfigPage/>
      </Box>
    </>
  );
}
