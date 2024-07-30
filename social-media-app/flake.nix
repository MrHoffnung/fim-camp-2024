{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = {
    self,
    nixpkgs,
    devenv,
    systems,
    ...
  } @ inputs: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
  in {
    packages = forEachSystem (system: {
      devenv-up = self.devShells.${system}.default.config.procfileScript;
    });

    devShells =
      forEachSystem
      (system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            {
              packages = [
              ];

              languages.python = {
                enable = true;
                package = pkgs.python311;
                poetry = {
                  enable = true;
                  package = pkgs.poetry.withPlugins (plugins:
                    with plugins; [
                      poetry-plugin-export
                    ]);
                };
              };

              pre-commit.hooks.alejandra.enable = true;

              pre-commit.hooks.black.enable = true;
              pre-commit.hooks.isort.enable = true;
              # needs to be fixed upstream to work with newer ruff versions
              # pre-commit.hooks.ruff.enable = false;

              pre-commit.hooks.djlint-lint = {
                enable = true;
                name = "Djlint";
                entry = "djlint";
                files = "^blog/templates/.*";
              };
              pre-commit.hooks.djlint-format = {
                enable = true;
                name = "Djlint formatting check";
                entry = "djlint --check";
                files = "^blog/templates/.*";
              };
            }
          ];
        };
      });
  };
}
