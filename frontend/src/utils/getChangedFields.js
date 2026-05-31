export const getChangedFields = (original, current) => {
  const changes = {};

  Object.keys(current).forEach((key) => {
    if (JSON.stringify(original[key]) !== JSON.stringify(current[key])) {
      changes[key] = current[key];
    }
  });

  return changes;
};
