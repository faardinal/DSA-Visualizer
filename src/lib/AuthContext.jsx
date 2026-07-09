import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // This project is intended to run publicly on deployed hosts where Replit/Base44
  // globals (and the full auth stack) are not available. The previous AuthContext
  // referenced createAxiosClient (missing at runtime) and attempted to load app
  // public settings on mount, which could crash the app.
  //
  // For production deployments, keep auth context safe and inert.
  const value = useMemo(() => {
    return {
      user: null,
      isAuthenticated: true,
      isLoadingAuth: false,
      isLoadingPublicSettings: false,
      authError: null,
      appPublicSettings: null,
      authChecked: true,
      logout: () => {},
      navigateToLogin: () => {},
      checkUserAuth: async () => {},
      checkAppState: async () => {},
    };
  }, []);

  // Preserve structure expected by the app: no-op mount effect.
  const [, forceRerender] = useState(0);
  useEffect(() => {
    // No auth bootstrap needed for public deployments.
    // Force a rerender once to match prior timing semantics if needed.
    forceRerender((x) => x);
  }, []);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

