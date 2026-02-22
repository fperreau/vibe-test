# incus-NAS

peux-tu m'expliquer comment fonctionne la commande "incus admin os system poweroff' dans ce projet github lxd/incus-os ?
je débute en golang et je voudrais comprendre comment ajouter d'autre commande en ligne.

---

```code
# incus/nas/create/*
incus nas list
incus nas create <nas1> --size="10GB" --description="Mon NAS"
incus nas use <nas1>
incus nas unuse
incus nas remove <nas1>

# incus/nas/user/*
incus nas user list
incus nas user create <fred> --password=""
incus nas user remove <fred>
incus nas user group <fred> --group="users"

# incus/nas/share/*
incus nas share list
incus nas share create <share1> --type="cifs" --source="/mnt/<share1>"
incus nas share remove <share1>
incus nas share owner <share1> --user="<fred>" --group="users" --mode="0770"
```
