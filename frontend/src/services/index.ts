// Mock services for now
export const useGetCurrentUserQuery = () => ({
  data: null,
  isLoading: false,
  error: null,
});

export const useLogoutMutation = () => ({
  mutate: () => {},
  isLoading: false,
});
