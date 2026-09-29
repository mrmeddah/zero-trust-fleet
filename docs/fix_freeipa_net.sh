#!/bin/bash
# A coller dans la console de la VM FreeIPA (root)
# Detection de l'interface par MAC, puis adressage statique 10.10.10.10

MAC_LAN="52:54:00:9e:df:02"   # vnet6 -> virbr-lan (segment VLAN 10)
IP="10.10.10.10/24"
GW="10.10.10.1"

echo "=== 1. Interfaces presentes ==="
ip -o link show | awk -F': ' '{print "   ", $2, $(NF-2), $NF}'

IFACE=""
for i in $(ls /sys/class/net); do
  m=$(cat /sys/class/net/$i/address 2>/dev/null)
  if [ "$m" = "$MAC_LAN" ]; then IFACE="$i"; fi
done

if [ -z "$IFACE" ]; then
  echo "!! Interface avec MAC $MAC_LAN introuvable."
  echo "!! Interfaces trouvees :"
  for i in $(ls /sys/class/net); do
    echo "     $i -> $(cat /sys/class/net/$i/address)"
  done
  exit 1
fi
echo "=== 2. Interface LAN detectee : $IFACE ==="

echo "=== 3. Configuration reseau ==="
if command -v nmcli >/dev/null 2>&1; then
  echo "   -> NetworkManager"
  nmcli con delete "ipa-lan-static" 2>/dev/null
  nmcli con add type ethernet ifname "$IFACE" con-name "ipa-lan-static" \
     ipv4.method manual ipv4.addresses "$IP" ipv4.gateway "$GW" \
     ipv4.dns "10.10.10.1" ipv4.never-default no \
     2>&1 | sed 's/^/     /'
  nmcli con up "ipa-lan-static" 2>&1 | sed 's/^/     /'
  nmcli dev set "$IFACE" managed yes 2>/dev/null
else
  echo "   -> network-scripts (CentOS/RHEL)"
  cat > /etc/sysconfig/network-scripts/ifcfg-ipa-lan <<EOF
DEVICE=$IFACE
NAME=ipa-lan
TYPE=Ethernet
BOOTPROTO=none
IPADDR=10.10.10.10
PREFIX=24
GATEWAY=10.10.10.1
DNS1=10.10.10.1
ONBOOT=yes
EOF
  systemctl restart network 2>&1 | sed 's/^/     /'
fi

echo "=== 4. Resultat ==="
ip -4 addr show "$IFACE" | sed 's/^/   /'
ip route | sed 's/^/   /'

echo "=== 5. Test de joignabilite ==="
ping -c3 -W2 10.10.10.1 2>&1 | tail -3 | sed 's/^/   /'

echo "=== 6. Etat des services IPA ==="
ipactl status 2>&1 | head -20 | sed 's/^/   /'
